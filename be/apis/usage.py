import datetime
import be.repository.access as dbaccess
import be.apis.pricing as pricinglib

usage_store = dbaccess.stores.usage_store

class UsageCollection:

    def new(self, resource_id, resource_name, member, start_time, created_by, end_time=None, quantity=None, cost=None, tax_dict={}, invoice=None, cancelled_against=None, pricing=None, booking=None, calculated_cost=None):

        if not quantity: quantity = 1
        if not end_time: end_time = start_time

        created = datetime.datetime.now()
        
        if not cancelled_against:
            calculated_cost = pricinglib.calculate_cost(**dict(member_id=member, resource_id=resource_id, quantity=quantity, starts=start_time, ends=end_time, cost=cost))
        if not cost: cost = calculated_cost
        data = dict(resource_id=resource_id, resource_name=resource_name, quantity=quantity, booking=booking, calculated_cost=calculated_cost, cost=cost, tax_dict=tax_dict, invoice=invoice, start_time=start_time, end_time=end_time, member=member, created_by=created_by, created=created, cancelled_against=cancelled_against, pricing=pricing)
        return usage_store.add(**data)

    def _delete(self, usage_id):
        """
        Delete a usage.
        """
        return usage_store.remove(usage_id)

    def cancel(self, usage_id, cancelled_by, amount=None):
        data = usage_store.get(usage_id)
        data['created_by'] = cancelled_by
        data['cancelled_against'] = usage_id
        data['cost'] = -data['cost']
        del(data['id'])
        del(data['created'])
        del(data['invoice'])
        if amount: usage_store.update(usage_id, cost=amount)
        return self.new(**data)
        
    def delete(self, usage_id, cancelled_by, amount=None):
        return self.cancel(usage_id, cancelled_by, amount) if usage_store.get(usage_id, 'invoice') else self._delete(usage_id) 

    def find(self, start=None, end=None, invoice_id=None, res_owner_ids=[], resource_ids=[], member_ids=[], resource_types=[], uninvoiced=False):
        """
        returns list of usage dicts which are filtered on the basis of specified criteria
        start end: if specified, usages with start time falling in start-end range would be searched
        """
        assert (start or end or invoice_id or res_owner_ids or resource_ids or member_ids or resource_types), 'atleast one criteria'
        return dbaccess.find_usage(start, end, invoice_id, res_owner_ids, resource_ids, member_ids, resource_types, uninvoiced)

class UsageResource:

    def info(self, usage_id):
        """
        return dict containg information of usage
        """
        return usage_store.get(usage_id)

    def update(self, usage_id, **mod_data):
        usage_store.update(usage_id, **mod_data)

    def get(self, usage_id, attrname):
        """
        return value of attrname
        """
        return usage_store.get(usage_id, fields=[attrname])

usage_collection = UsageCollection()
usage_resource = UsageResource()
