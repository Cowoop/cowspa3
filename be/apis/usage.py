import datetime
import itertools
import be.repository.access as dbaccess
import be.apis.pricing as pricinglib
import be.apis.resource as resourcelib
import be.apis.billingpref as billingpreflib

usage_store = dbaccess.stores.usage_store
member_store = dbaccess.stores.member_store

class UsageCollection:

    def new(self, resource_id, resource_name, resource_owner, member, start_time, end_time=None, quantity=1, cost=None, tax_dict={}, invoice=None, cancelled_against=None, calculated_cost=None, name=None, notes=None, description=None):

        if not end_time: end_time = start_time
        created = datetime.datetime.now()

        if cancelled_against:
            total = cost
        else:
            result = pricinglib.calculate_cost(member_id=member, resource_id=resource_id, resource_owner=resource_owner, quantity=quantity, starts=start_time, ends=end_time, cost=cost, return_taxes=True)
            calculated_cost = result['calculated_cost']
            total = result['total']
            tax_dict = result['taxes']
            if cost is None:
                cost = calculated_cost

        pricing = pricinglib.pricings.get(member, resource_id, start_time) if resource_id else None
        data = dict(resource_id=resource_id, resource_name=resource_name, resource_owner=resource_owner, quantity=quantity, calculated_cost=calculated_cost, cost=cost, total=total, tax_dict=tax_dict, invoice=invoice, start_time=start_time, end_time=end_time, member=member, created_by=env.context.user_id, created=created, cancelled_against=cancelled_against, pricing=pricing, name=name, notes=notes, description=description)
        return usage_store.add(**data)

    def m_new(self, resource_id, resource_name, resource_owner, member, start_time, total=None, end_time=None, quantity=1, cost=None, invoice=None, cancelled_against=None, calculated_cost=None, created=None, name=None, notes=None, description=None):

        if not end_time: end_time = start_time
        data = dict(resource_id=resource_id, resource_name=resource_name, resource_owner=resource_owner, quantity=quantity, calculated_cost=calculated_cost, cost=cost, total=total, invoice=invoice, start_time=start_time, end_time=end_time, member=member, created_by=env.context.user_id, created=created, cancelled_against=cancelled_against, name=name, notes=notes)
        return usage_store.add(**data)

    def _delete(self, usage_id):
        """
        Delete a usage.
        """
        return usage_store.remove(usage_id)

    def cancel(self, usage_id):
        data = usage_store.get(usage_id)
        data['cancelled_against'] = usage_id
        data['cost'] = -data['total']
        del(data['created_by'])
        del(data['id'])
        del(data['total'])
        del(data['created'])
        del(data['invoice'])
        del(data['pricing'])
        return self.new(**data)

    def delete(self, usage_id):
        return self.cancel(usage_id) if usage_store.get(usage_id, 'invoice') else self._delete(usage_id)

    def bulk_delete(self, usage_ids):
        for usage_id in usage_ids:
            self.delete(usage_id)
        return True

    def find(self, start=None, end=None, invoice_id=None, res_owner_ids=[], resource_ids=[], member_ids=[], resource_types=[], uninvoiced=False, exclude_credit_usages=False, calc_mode=[], exclude_cancelled_usages=False):
        """
        returns list of usage dicts which are filtered on the basis of specified criteria
        start end: if specified, usages with start time falling in start-end range would be searched
        """
        assert (start or end or invoice_id or res_owner_ids or resource_ids or member_ids or resource_types), 'atleast one criteria'
        return dbaccess.find_usage(start, end, invoice_id, res_owner_ids, resource_ids, member_ids, resource_types, uninvoiced, exclude_credit_usages, calc_mode, exclude_cancelled_usages)

    def uninvoiced(self, member_id, res_owner_id, start, end):
        member_ids = dbaccess.get_billto_members(member_id)
        return self.find(start=start, end=end, res_owner_ids=[res_owner_id], member_ids=member_ids, uninvoiced=True)

    def find_by_date(self, *args, **kw):
        bookings = self.find(*args, **kw)
        grouper = lambda b: b.start_time.date()
        return [dict(date=date, bookings=tuple(g)) for date, g in itertools.groupby(bookings, grouper)]

class UsageResource:

    def info(self, usage_id):
        """
        return dict containg information of usage
        """
        usage = usage_store.get(usage_id)
        usage['member_name'] = dbaccess.oid2name(usage.member)
        return usage

    def update(self, usage_id, **mod_data):
        # attrs that force cost recalculation
        cost_affecting_attrs = set(('start_time', 'end_time', 'resource_id', 'quantity', 'member'))
        recalculate = bool(cost_affecting_attrs.intersection(mod_data.keys()))
        usage = self.info(usage_id)
        recalculate = recalculate and not usage.cancelled_against

        if recalculate:
            usage_data = dict(member_id=mod_data.get('member', usage.member),
                resource_id=mod_data.get('resource_id', usage.resource_id),
                resource_owner=mod_data.get('resource_owner', usage.resource_owner),
                quantity=mod_data.get('quantity', usage.quantity),
                starts=mod_data.get('start_time', usage.start_time),
                ends=mod_data.get('end_time', usage.end_time) )
            result = pricinglib.calculate_cost(return_taxes=True, **usage_data)
            mod_data.update(calculated_cost = result['calculated_cost'],
                total = result['total'],
                tax_dict = result['taxes'],
                pricing = pricinglib.pricings.get(usage.member, usage.resource_id, usage.start_time) if usage.resource_id else None)

        if not 'cost' in mod_data and recalculate and usage.cost == usage.calculated_cost:
            mod_data['cost'] = mod_data['calculated_cost']

        usage_store.update(usage_id, **mod_data)

    def get(self, usage_id, attrname):
        """
        return value of attrname
        """
        return usage_store.get(usage_id, fields=[attrname])

usage_collection = UsageCollection()
usage_resource = UsageResource()
