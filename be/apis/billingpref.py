import datetime
import be.repository.access as dbaccess
import be.apis.activities as activitylib
import commonlib.helpers

member_store = dbaccess.stores.member_store
billingpref_store = dbaccess.stores.billingpref_store
modes = commonlib.helpers.odict(**{'self':0, 'custom':1, 'another':2, 'business':3})

class BillingprefCollection:
    def new(self, member, mode=modes.self, billto=None, details=None):

        data = dict(member=member, mode=mode, billto=billto, details=details)
        billingpref_store.add(**data)

        return True
        
class BillingprefResource:

    def update(self, member, **mod_data):
        
        if mod_data['mode'] == modes.business and not mod_data['billto']:
            mod_data['billto'] = bizlib.biz_collection.new(**mod_data['biz_details'])
            del mod_data['biz_details']
        billingpref_store.update_by(dict(member=member), **mod_data)
        
        data = dict(name=member_store.get(member, ['name']), member_id=member)
        activity_id = activitylib.add('billingpref_management', 'billingpref_updated', data)
        
        return True
   
    def get_details(self, member):
        
        billto = member
        while True:
            preferences = self.info(billto)
            billto = preferences['billto'] if preferences['mode'] != modes.self else billto
            details = preferences['details'] if billto != member or preferences['mode'] != modes.another else None
            mode = preferences['mode'] if billto != member or preferences['mode'] != modes.another else modes.self
            if mode == modes.self:
                details = member_store.get(billto, ['name', 'address', 'city', 'country', 'phone', 'email'])
                break
            elif mode == modes.custom:
                break
            elif mode == modes.another:
                continue
            elif mode == modes.business:
                details = biz_store.get(billto, ['name', 'address', 'city', 'country', 'phone', 'email'])
                break
        return details
        
    def info(self, member):
        return billingpref_store.get_by(dict(member=member), fields=['mode', 'billto', 'details'])[0]

billingpref_resource = BillingprefResource()
billingpref_collection = BillingprefCollection()
