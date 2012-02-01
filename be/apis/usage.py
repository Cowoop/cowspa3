import datetime
import itertools
import be.repository.access as dbaccess
import be.apis.pricing as pricinglib
import be.apis.resource as resourcelib
import be.apis.billingpref as billingpreflib

usage_store = dbaccess.stores.usage_store

class UsageCollection:

    def new(self, resource_id, resource_name, resource_owner, member, start_time, amount=None, end_time=None, quantity=1, cost=None, tax_dict={}, invoice=None, cancelled_against=None, pricing=None, calculated_cost=None):

        if not end_time: end_time = start_time
        created = datetime.datetime.now()

        if not cancelled_against:
            result = pricinglib.calculate_cost(**dict(member_id=member, resource_id=resource_id, resource_owner=resource_owner, quantity=quantity, starts=start_time, ends=end_time, cost=cost, return_taxes=True))
            calculated_cost = result['calculated_cost']
            amount = result['amount']
            tax_dict = result['taxes']
        if cost is None: cost = calculated_cost
        data = dict(resource_id=resource_id, resource_name=resource_name, resource_owner=resource_owner, quantity=quantity, calculated_cost=calculated_cost, cost=cost, amount=amount, tax_dict=tax_dict, invoice=invoice, start_time=start_time, end_time=end_time, member=member, created_by=env.context.user_id, created=created, cancelled_against=cancelled_against, pricing=pricing)
        return usage_store.add(**data)

    def m_new(self, resource_id, resource_name, resource_owner, member, start_time, amount=None, end_time=None, quantity=1, cost=None, invoice=None, cancelled_against=None, pricing=None, calculated_cost=None, created=None):

        if not end_time: end_time = start_time
        tax_dict = {}
        if not cost: cost = calculated_cost
        data = dict(resource_id=resource_id, resource_name=resource_name, resource_owner=resource_owner, quantity=quantity, calculated_cost=calculated_cost, cost=cost, amount=amount, tax_dict=tax_dict, invoice=invoice, start_time=start_time, end_time=end_time, member=member, created_by=env.context.user_id, created=created, cancelled_against=cancelled_against, pricing=pricing)
        return usage_store.add(**data)

    def _delete(self, usage_id):
        """
        Delete a usage.
        """
        return usage_store.remove(usage_id)

    def cancel(self, usage_id, amount=None):
        data = usage_store.get(usage_id)
        data['cancelled_against'] = usage_id
        data['cost'] = -data['cost']
        del(data['created_by'])
        del(data['id'])
        del(data['created'])
        del(data['invoice'])
        if data['tax_dict']:
            for tax in data['tax_dict']:
                data['tax_dict'][tax] = -data['tax_dict'][tax]
        if amount: usage_store.update(usage_id, cost=amount)
        return self.new(**data)

    def delete(self, usage_id, amount=None):
        return self.cancel(usage_id, amount) if usage_store.get(usage_id, 'invoice') else self._delete(usage_id)

    def bulk_delete(self, usage_ids, amount=None):
        for usage_id in usage_ids:
            self.delete(usage_id, amount)
        return True

    def find(self, start=None, end=None, invoice_id=None, res_owner_ids=[], resource_ids=[], member_ids=[], resource_types=[], uninvoiced=False, exclude_credit_usages=False, calc_mode=[], exclude_cancelled_usages=False, get_dependent_usages=False):
        """
        returns list of usage dicts which are filtered on the basis of specified criteria
        start end: if specified, usages with start time falling in start-end range would be searched
        """
        if get_dependent_usages:
            billing_info = billingpreflib.billingpref_resource.info(member_ids[0])
            if billing_info['mode'] == 2: return []
            member_ids = billingpreflib.billingpref_resource.get_dependent_members(member_ids[0])
        assert (start or end or invoice_id or res_owner_ids or resource_ids or member_ids or resource_types), 'atleast one criteria'
        return dbaccess.find_usage(start, end, invoice_id, res_owner_ids, resource_ids, member_ids, resource_types, uninvoiced, exclude_credit_usages, calc_mode, exclude_cancelled_usages)

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
        usage_store.update(usage_id, **mod_data)

    def get(self, usage_id, attrname):
        """
        return value of attrname
        """
        return usage_store.get(usage_id, fields=[attrname])

usage_collection = UsageCollection()
usage_resource = UsageResource()
