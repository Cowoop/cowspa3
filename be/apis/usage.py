import datetime
import be.repository.access as dbaccess

usage_store = dbaccess.stores.usage_store

class UsageCollection:

    def new(self, resource_name, rate, quantity, calculated_cost, member, start_time, cost=None, tax_dict={}, invoice=None, resource_id=None, end_time=None):
        if not cost: cost = calculated_cost
        created = datetime.datetime.now()
        if not end_time: end_time = start_time
        data = dict(resource_id=resource_id, resource_name=resource_name, rate=rate, quantity=quantity, calculated_cost=calculated_cost, cost=cost, tax_dict=tax_dict, invoice=invoice, start_time=start_time, end_time=end_time, member=member, created=created)
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
        result = usage_store.get(usage_id)
        result['start_time'] = result['start_time'].isoformat()
        result['end_time'] = result['end_time'].isoformat() if result['end_time'] else result['end_time']
        return result

    def update(self, usage_id, mod_data):
        usage_store.update(usage_id, **mod_data)

    def get(self, usage_id, attrname):
        """
        return value of attrname
        """
        result = usage_store.get(usage_id, fields=[attrname])
        if (attrname == 'start_time' or attrname == 'end_time') and result:
            result = result.isoformat()
        return result

    def find(self, start=None, end=None, res_owner_refs=[], resource_ids=[], member_ids=[], resource_types=[]):
        """
        return list of dicts which contains information of usage, which are sorted on the basis of selected criteria like start time, end time, resource ids, resource owner references, member ids or resource types
        """
        return dbaccess.find_usage(start, end, res_owner_refs, resource_ids, member_ids, resource_types)


usage_collection = UsageCollection()
usage_resource = UsageResource()
