import datetime
import be.repository.access as dbaccess
import be.apis.pricing as pricinglib

usage_store = dbaccess.stores.usage_store

class UsageCollection:

    def new(self, resource_id, resource_name, quantity, cost, member, start_time, end_time=None, tax_dict={}, invoice=None):

        created = datetime.datetime.now()
        calculated_cost = pricinglib.calculate_cost(**dict(member_id=member, resource_id=resource_id, quantity=quantity, starts=start_time, ends=end_time))
        if not end_time: end_time = start_time
        data = dict(resource_id=resource_id, resource_name=resource_name, quantity=quantity, calculated_cost=calculated_cost, cost=cost, tax_dict=tax_dict, invoice=invoice, start_time=start_time, end_time=end_time, member=member, created=created)
        usage_id = usage_store.add(**data)
        return usage_id

    def delete(self, usage_id):
        """
        Delete a usage.
        """
        return usage_store.remove(usage_id)

    def find(self, start=None, end=None, invoice=None, res_owner_refs=[], resource_ids=[], member_ids=[], resource_types=[], fields=None, hashrows=True):
        """
        return list of dicts which contains information of usage, which are sorted on the basis of selected criteria like start time, end time, resource ids, resource owner references, member ids or resource types
        """
        return dbaccess.find_usage(start, end, invoice, res_owner_refs, resource_ids, member_ids, resource_types, fields, hashrows=hashrows)

class UsageResource:

    def info(self, usage_id):
        """
        return dict containg information of usage
        """
        return usage_store.get(usage_id)

    def update(self, usage_id, mod_data):
        usage_store.update(usage_id, **mod_data)

    def get(self, usage_id, attrname):
        """
        return value of attrname
        """
        return usage_store.get(usage_id, fields=[attrname])

usage_collection = UsageCollection()
usage_resource = UsageResource()
