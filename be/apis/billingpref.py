import datetime
import be.repository.access as dbaccess
import be.apis.activities as activitylib
import be.apis.biz as bizlib
import commonlib.helpers

member_store = dbaccess.stores.member_store
biz_store = dbaccess.stores.biz_store
billingpref_store = dbaccess.stores.billingpref_store

class BillingprefCollection:
    def new(self, member, mode=0, billto=None, details=None):

        data = dict(member=member, mode=mode, billto=billto, details=details)
        billingpref_store.add(**data)

        return True
        
class BillingprefResource:

    def update(self, member, **mod_data):
        
        if mod_data['mode'] == 1 and not mod_data['billto']:
            mod_data['billto'] = bizlib.biz_collection.new(**mod_data['details'])
            mod_data['details'] = None
        billingpref_store.update_by(dict(member=member), **mod_data)
        
        data = dict(name=member_store.get(member, ['display_name']), member_id=member)
        activity_id = activitylib.add('billingpref_management', 'billingpref_updated', data)
        
        return True
   
    def get_billing_preferences_details(self, member):
        
        modes = commonlib.helpers.odict(**{'self':0, 'bizness':1, 'another':2})
        details = None
        billto = member
        mode = modes.another
        while True:
            if mode == modes.self:
                if not details:
                    details = member_store.get(member,['display_name', 'phone', 'email'])
                    details['name'] = details['display_name']
                    del details['display_name'] 
                break                
            elif mode == modes.bizness:
                details = biz_store.get(biz,['name', 'phone', 'email'])
                break
            elif mode == modes.another:
                preferences = self.get(billto) 
            mode = preferences['mode'] if billto != member else modes.self
            billto = preferences['billto']
            details = preferences['details'] 
        return details
        
    def info(self, member):
        return billingpref_store.get_by(dict(member=member), fields=['mode', 'billto', 'details'])[0]

billingpref_resource = BillingprefResource()
billingpref_collection = BillingprefCollection()
