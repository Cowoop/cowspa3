import datetime
import be.repository.access as dbaccess
import be.apis.pricing as pricinglib

usage_store = dbaccess.stores.usage_store

class UsageCollection:

    def new(self, resource_id, resource_name, quantity, cost, member, start_time, end_time=None, tax_dict={}, invoice=None):

        created = datetime.datetime.now()
        if not end_time: end_time = start_time
        calculated_cost = pricinglib.calculate_cost(**dict(member_id=member, resource_id=resource_id, quantity=quantity, starts=start_time, ends=end_time))
        data = dict(resource_id=resource_id, resource_name=resource_name, quantity=quantity, calculated_cost=calculated_cost, cost=cost, tax_dict=tax_dict, invoice=invoice, start_time=start_time, end_time=end_time, member=member, created=created)
        usage_id = usage_store.add(**data)
        return usage_id

    def delete(self, usage_id):
        """
        Delete a usage.
        """
        return usage_store.remove(usage_id)

    def find(self, start=None, end=None, invoice_id=None, res_owner_ids=[], resource_ids=[], member_ids=[], resource_types=[]):
        """
        returns list of usage dicts which are filtered on the basis of specified criteria
        start end: if specified, usages with start time falling in start-end range would be searched
        """
        assert (start or end or invoice_id or res_owner_ids or resource_ids or member_ids or resource_types), 'atleast one criteria'
        return dbaccess.find_usage(start, end, invoice_id, res_owner_ids, resource_ids, member_ids, resource_types)

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
