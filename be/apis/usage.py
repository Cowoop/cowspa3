import datetime
import be.repository.access as dbaccess

usage_store = dbaccess.usage_store

class UsageCollection:

    def add(self, resource_name, calculated_cost, cost, tax_dict, member, start_time, invoice=None, resource_id=None, end_time=None):
        
        created = datetime.datetime.now()
        if not end_time:
            end_time = start_time
        data = dict(resource_id=resource_id, resource_name=resource_name, calculated_cost=calculated_cost, cost=cost, tax_dict=tax_dict, invoice=invoice, start_time=start_time, end_time=end_time, member=member, created=created)
        usage_id = usage_store.add(**data)
        return usage_id

    def delete(self, usage_id):
        """
        Delete a usage.
        """
        return usage_store.remove(usage_id)

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
        
    def find(self, start=None, end=None, res_owner_refs=[], resource_ids=[], member_ids=[], resource_types=[]):
        """
        return list of dicts which contains information of usage, which are sorted on the basis of selected criteria like start time, end time,
        resource ids, resource owner references, member ids or resource types  
        """
        return dbaccess.find_usage(start, end, res_owner_refs, resource_ids, member_ids, resource_types)
        

usage_collection = UsageCollection()
usage_resource = UsageResource()
