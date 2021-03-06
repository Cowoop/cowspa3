import datetime
import psycopg2

import commonlib.helpers
import be.errors
import be.repository.access as dbaccess
import be.apis.pricing as pricinglib
import be.apis.resource as resourcelib
import be.apis.billingpref as billingpreflib
import be.apis.messagecust as messagecustlib
import be.apis.activities as activitylib
import be.libs.cost as costlib

usage_store = dbaccess.stores.usage_store
member_store = dbaccess.stores.member_store
bizplace_store = dbaccess.stores.bizplace_store
bookingslot_store = dbaccess.stores.bookingslot_store

interval = 1 # one minute

def gen_slot_ids(resource_id, start, end):
    """
    """
    start = commonlib.helpers.iso2datetime(start)
    end = commonlib.helpers.iso2datetime(end)

    slot_ids = []
    delta = end - start
    next_ = start
    fmt = str(resource_id) + '%Y%m%d%H%M'
    while next_ < end:
        slot_ids.append(next_.strftime(fmt))
        next_ += datetime.timedelta(0, interval*60)
    return slot_ids

def reserve_slots(booking_id, resource_id, start, end):
    """
    raises Exception on failing to reserve a slot
    """
    slot_ids = gen_slot_ids(resource_id, start, end)
    slots = [dict(id=id, booking=booking_id) for id in slot_ids]
    try:
        bookingslot_store.add_many(slots)
    except psycopg2.IntegrityError:
        raise be.errors.ErrorWithHint('Time slot conflicts with other booking')

def release_slots(booking_id):
    """
    tries to find slots and removes if there are
    """
    bookingslot_store.remove_by(crit=dict(booking=booking_id))

def update_slots(booking_id, resource_id, start, end):
    release_slots(booking_id)
    reserve_slots(booking_id, resource_id, start, end)

def add_suggested_usages(resource_owner, suggesting_usage, suggested_resources, usages):
    suggested_usages_data = []
    usages_dict = dict((usage['resource_id'], usage) for usage in usages)
    start_time = suggesting_usage['start_time']
    start_time = start_time.isoformat() if isinstance(start_time, datetime.datetime) else start_time
    end_time = suggesting_usage['end_time']
    end_time = end_time.isoformat() if isinstance(end_time, datetime.datetime) else end_time
    for resource in suggested_resources:
        if resource.id in usages_dict:
            usage = usages_dict[resource.id]
            new_data = dict(resource_id=resource.id,
                resource_name=resource.name,
                resource_owner=resource_owner,
                member=suggesting_usage['member'],
                start_time=start_time,
                end_time=(start_time if resource.calc_mode == resourcelib.CalcMode.quantity_based else end_time),
                quantity=usage.get('quantity', 1))
            suggested_usages_data.append(new_data)
    return [usage_collection.new(**new_data) for new_data in suggested_usages_data]

def allow_cancel(usage):
    allow = False
    ctx_roles = env.context.current_roles.get(usage.resource_owner, None)
    if ctx_roles:
        if set(['director', 'host']).intersection(ctx_roles.role_names):
            allow = True
        elif usage.member == env.context.user_id and (usage.start_time - datetime.datetime.now()) > datetime.timedelta(14):
            allow = True
    return allow

class UsageCollection:

    def new(self, resource_id, resource_name, resource_owner, member, start_time, end_time=None, quantity=1, cost=None, tax_dict={}, invoice=None, cancelled_against=None, calculated_cost=None, notes=None, usages=[], name=None, description=None, no_of_people=0, suppress_notification=False, public=False, repetition_id=None):
        # TODO shouldn't we name the parameter member_id and not member

        if quantity is None: quantity = 1
        if not end_time: end_time = start_time

        resource = resourcelib.resource_resource.info(resource_id) if resource_id else None
        member_dict = member_store.get(member, ['id', 'first_name', 'name', 'email'])
        if resource:
            resource_owner = resource.owner
            if not resource.enabled or resource.archived:
                raise be.errors.ErrorWithHint('Resource is either not enabled or is archived')

        if end_time < start_time:
            raise be.errors.ErrorWithHint('Start time is less than end time')
        created = datetime.datetime.now()

        if cancelled_against:
            total = cost + costlib.to_decimal(tax_dict.get('total', 0))
        else:
            result = pricinglib.calculate_cost(member_id=member, resource_id=resource_id, resource_owner=resource_owner, quantity=quantity, starts=start_time, ends=end_time, cost=cost, return_taxes=True)
            calculated_cost = result['calculated_cost']
            total = result['total']
            tax_dict = result['taxes']
            if cost is None:
                cost = calculated_cost

        pricing = pricinglib.pricings.get(member, resource_id, start_time) if resource_id else None
        data = dict(resource_id=resource_id, resource_name=resource_name, resource_owner=resource_owner, quantity=quantity, calculated_cost=calculated_cost, cost=cost, total=total, tax_dict=tax_dict, invoice=invoice, start_time=start_time, end_time=end_time, member=member, created_by=env.context.user_id, created=created, cancelled_against=cancelled_against, pricing=pricing, notes=notes, name=name, description=description, no_of_people=no_of_people, public=public, repetition_id=repetition_id)
        if resource and (resource.calc_mode == resourcelib.CalcMode.quantity_based):
            data['end_time'] == start_time
        else:
            data['quantity'] == 1

        if not cancelled_against and not resource_id == 0:
            usages_dict = dict((usage['resource_id'], usage) for usage in usages)
            relations = resourcelib.resource_resource.get_relations(resource_id)
            contained_usages_data = []
            suggested_usages_data = []

            for res in relations[True]:
                usage = usages_dict.get(res.id, {})
                new_data = dict(resource_id=res.id,
                    resource_name=res.name,
                    resource_owner=resource_owner,
                    member=member,
                    suppress_notification=True,
                    start_time=start_time,
                    end_time=start_time if res.calc_mode == resourcelib.CalcMode.quantity_based else data['end_time'],
                    quantity=usage.get('quantity', 1))
                contained_usages_data.append(new_data)

            contained_usage_ids = [self.new(**new_data) for new_data in contained_usages_data]
            suggested_usage_ids = add_suggested_usages(resource['owner_id'], data, relations[False], usages)

            also_booked_text = ', '.join(res.name for res in relations[False] if res.id in usages_dict)

            data['usages_contained'] = contained_usage_ids
            data['usages_suggested'] = suggested_usage_ids

        usage_id = usage_store.add(**data)


        if resource and resource.calc_mode == resourcelib.CalcMode.time_based:
            reserve_slots(usage_id, resource.id, start_time, end_time)

        suppress_email = cancelled_against or suppress_notification or resource_id == 0 or \
            (resource and resource.calc_mode != resourcelib.CalcMode.time_based)
        if not suppress_email:
            owner = bizplace_store.get(resource_owner, ['id', 'name', 'booking_email', 'currency', 'host_email', 'phone'])

            also_booked_text = 'Also booked: ' + also_booked_text if also_booked_text else ''
            email_data = dict(LOCATION=owner.name, MEMBER_EMAIL=member_dict.email, BOOKING_CONTACT=owner.booking_email or owner.host_email, MEMBER_FIRST_NAME=member_dict.first_name, RESOURCE=resource_name, BOOKING_START=commonlib.helpers.time4human(start_time), BOOKING_END=commonlib.helpers.time4human(end_time), BOOKING_DATE=commonlib.helpers.date4human(start_time), CURRENCY=owner.currency, COST=cost, HOSTS_EMAIL=owner.host_email, LOCATION_PHONE=owner.phone)
            mailtext = messagecustlib.get(owner.id, 'booking_confirmation')
            notification = commonlib.messaging.messages.booking_confirmation(email_data, overrides=dict(plain=mailtext, bcc='cowspa.dev@gmail.com'))
            notification.build()
            notification.email()

        a_data = dict(resource_id=resource_id, resource_name=resource_name, resource_owner=resource_owner, member_id=member_dict.id, member_name=member_dict.name, start_time=start_time, end_time=end_time, actor_id=env.context.user_id, actor_name=env.context.name, created=created)
        activity_id = activitylib.add('booking', 'booking_created', a_data, created)

        return usage_id

    def m_new(self, resource_id, resource_name, resource_owner, member, start_time, total=None, end_time=None, quantity=1, cost=None, invoice=None, cancelled_against=None, calculated_cost=None, created=None, notes=None, name=None, description=None, no_of_people=0, repetition_id=None, public=False):

        if not end_time: end_time = start_time
        if cost is None: cost = calculated_cost
        data = dict(resource_id=resource_id, resource_name=resource_name, resource_owner=resource_owner, quantity=quantity, calculated_cost=calculated_cost, cost=cost, total=total, invoice=invoice, start_time=start_time, end_time=end_time, member=member, created_by=env.context.user_id, created=created, cancelled_against=cancelled_against, name=name, notes=notes, repetition_id=repetition_id, public=public, description=description, no_of_people=no_of_people)

        return usage_store.add(**data)

    def _delete(self, usage_id):
        """
        Delete a usage.
        """
        release_slots(usage_id)
        return usage_store.remove(usage_id)

    def cancel(self, usage_id):
        if usage_store.get_by(crit=dict(cancelled_against=usage_id)):
            raise be.errors.ErrorWithHint('Usage [%s] is already canceled' % usage_id)
        data = usage_store.get(usage_id)
        data['cancelled_against'] = usage_id
        data['cost'] = -data['cost']
        new_tax_dict = dict(total=-data['tax_dict']['total'])
        new_tax_dict['breakdown'] = tuple((name, level, -amount) for (name, level, amount) in data['tax_dict']['breakdown'])
        data['tax_dict'] = new_tax_dict
        linked_usage_ids = (data['usages_suggested'] or []) + (data['usages_contained'] or [])
        self.bulk_delete(linked_usage_ids)
        del(data['usages_contained'])
        del(data['usages_suggested'])
        del(data['created_by'])
        del(data['id'])
        del(data['total'])
        del(data['created'])
        del(data['invoice'])
        del(data['pricing'])

        release_slots(usage_id)
        return self.new(**data)

    def delete(self, usage_id):
        usage = usage_store.get(usage_id, fields=['id', 'cancelled_against', 'invoice', 'usages_suggested', 'resource_owner'])
        if not allow_cancel(usage):
            raise be.errors.SecurityViolation("Usage delete action is not allowed")
        for suggested_usage_id in (usage.usages_suggested or []): # None guard
            self.delete(suggested_usage_id)
        suggesting_usage = dbaccess.find_suggesting_usage(usage_id)
        if suggesting_usage:
            suggesting_usage.usages_suggested.remove(usage_id)
            usage_store.update(suggesting_usage.id, usages_suggested=suggesting_usage.usages_suggested)
            # ^ calling usage.update will cause recursion
        if not usage.invoice:
            return self._delete(usage_id)
        else:
            if not usage.cancelled_against:
                return self.cancel(usage_id)
            else:
                raise Exception('Can not delete usage which is already invoiced and canceled')

    def bulk_delete(self, usage_ids):
        for usage_id in usage_ids:
            self.delete(usage_id)
        return True

    def find(self, start=None, end=None, starts_on_or_before=None, invoice_id=None, res_owner_ids=[], resource_ids=[], member_ids=[], resource_types=[], uninvoiced=False, exclude_credit_usages=False, calc_mode=[], exclude_cancelled_usages=False):
        """
        returns list of usage dicts which are filtered on the basis of specified criteria
        start end: if specified, usages with start time falling in start-end range would be searched
        """
        assert (start or end or invoice_id or res_owner_ids or resource_ids or member_ids or resource_types), 'atleast one criteria'
        return dbaccess.find_usage(start, end, starts_on_or_before, invoice_id, res_owner_ids, resource_ids, member_ids, resource_types, uninvoiced, exclude_credit_usages, calc_mode, exclude_cancelled_usages)

    def uninvoiced(self, member_id, res_owner_id, start, end):
        """
        find uninvoiced usages of a member
        """
        member_ids = dbaccess.get_billfrom_members(member_id)
        return self.find(start=start, end=end, res_owner_ids=[res_owner_id], member_ids=member_ids, uninvoiced=True)

    def uninvoiced_members(self, res_owner_id, start, zero_usage_members=False, only_tariff=False):
        """
        returns list members with uninvoiced usages total
        """
        find_crit = dict(res_owner_ids=[res_owner_id], starts_on_or_before=start, uninvoiced=True)
        if only_tariff:
            find_crit['resource_types'] = ['tariff']
        usages = self.find(**find_crit)
        member_ids = set(usage.member_id for usage in usages)
        member_billto_map = dbaccess.get_billto_members(member_ids)
        sorter = lambda usage: member_billto_map[usage.member_id]
        usages_grouped = [(billto_member, tuple(g)) for billto_member, g in commonlib.helpers.sortngroupby(usages, sorter)]
        member_names = dict((member.id, member.name) for member in \
            member_store.get_many(member_billto_map.values(), ['id', 'name']))
        result = [dict(member_name=member_names[m], member=m, usages=g, total=sum(usg.total for usg in g if usg.total)) for m, g in usages_grouped]
        if not zero_usage_members:
            result = [d for d in result if d['total']]
        return result

    def find_by_date(self, *args, **kw):
        bookings = self.find(*args, **kw)
        grouper = lambda b: b.start_time.date()
        return [dict(date=date, bookings=tuple(g)) for date, g in commonlib.helpers.sortngroupby(bookings, grouper)]

class UsageResource:

    def info(self, usage_id):
        """
        return dict containg information of usage
        """
        usage = usage_store.get(usage_id)
        usage['member_name'] = dbaccess.oid2name(usage.member)
        return usage

    def details(self, usage_id):
        usage = self.info(usage_id)
        usage['usages_suggested'] = usage_store.get_many(usage.usages_suggested, ['id', 'resource_id', 'start_time', 'end_time', 'quantity'])
        usage['cancel_allowed'] = allow_cancel(usage)
        return usage

    def update(self, usage_id, recalculate=False, **mod_data):
        usage = usage_store.get(usage_id)

        if not recalculate:
            # attrs that force cost recalculation
            cost_affecting_attrs = set(('start_time', 'end_time', 'resource_id', 'quantity', 'member', 'cost'))
            recalculate = bool(cost_affecting_attrs.intersection(mod_data.keys()))
            recalculate = recalculate and not usage.cancelled_against

        if recalculate:
            usage_data = dict(member_id=mod_data.get('member', usage.member),
                resource_id=mod_data.get('resource_id', usage.resource_id),
                resource_owner=mod_data.get('resource_owner', usage.resource_owner),
                quantity=mod_data.get('quantity', usage.quantity),
                starts=mod_data.get('start_time', usage.start_time),
                cost=mod_data.get('cost'),
                ends=mod_data.get('end_time', usage.end_time) )
            result = pricinglib.calculate_cost(return_taxes=True, **usage_data)
            mod_data.update(calculated_cost = result['calculated_cost'],
                total = result['total'],
                tax_dict = result['taxes'],
                pricing = pricinglib.pricings.get(usage.member, usage.resource_id, usage.start_time) if usage.resource_id else None)
            if not 'cost' in mod_data:
                if usage.cost is None:
                    mod_data['cost'] = result['calculated_cost']

        if 'usages' in mod_data:
            usages = mod_data.pop('usages')
            for suggested_usage_id in usage.usages_suggested:
                usage_collection.delete(suggested_usage_id)
            relations = resourcelib.resource_resource.get_relations(usage.resource_id)
            mod_data['usages_suggested'] = add_suggested_usages(usage.resource_owner, usage, relations[False], usages)

        if 'start_time' in mod_data or 'end_time' in mod_data:
            start_time = mod_data.get('start_time', usage.start_time)
            end_time = mod_data.get('end_time', usage.end_time)
            update_slots(usage_id, usage.resource_id, start_time, end_time)

        usage_store.update(usage_id, **mod_data)

    def get(self, usage_id, attrname):
        """
        return value of attrname
        """
        return usage_store.get(usage_id, fields=[attrname])

usage_collection = UsageCollection()
usage_resource = UsageResource()
