import datetime
import be.repository.access as dbaccess
import be.apis.activities as activitylib
import be.apis.member as memberlib
import commonlib.helpers

member_store = dbaccess.stores.member_store
invoicepref_store = dbaccess.stores.invoicepref_store

modes = commonlib.helpers.odict(self=0, custom=1, other=2, organization=3)

class BillingprefResource:

    def update(self, member, **mod_data):

        if mod_data['mode'] == modes.organization and not mod_data['billto']:
            mod_data['organization_details']['mtype'] = "organization"
            mod_data['billto'] = memberlib.member_collection.new(**mod_data['organization_details'])
            del mod_data['organization_details']
        if mod_data['mode'] == modes.other and mod_data['billto'] == member:
            mod_data['mode'] == modes.self
            del(mod_data['billto'])
        invoicepref_store.update_by(dict(member=member), **mod_data)

        data = dict(name=member_store.get(member, ['name']), member_id=member)
        activity_id = activitylib.add('billingpref_management', 'billingpref_updated', data)

        return True

    def get_details(self, member):

        billto = member
        while True:
            preferences = self.info(billto)
            billto = preferences['billto'] if preferences['mode'] != modes.self else billto
            details = preferences['details'] if billto != member or preferences['mode'] != modes.other else None
            mode = preferences['mode'] if billto != member or preferences['mode'] != modes.other else modes.self
            if mode == modes.self:
                details = member_store.get(billto, ['name', 'address', 'city', 'country', 'phone', 'email'])
                break
            elif mode == modes.custom:
                break
            elif mode == modes.other:
                continue
            elif mode == modes.organization:
                details = member_store.get(billto, ['name', 'address', 'city', 'country', 'phone', 'email'])
                break
        return details

    def info(self, member):
        return invoicepref_store.get_by(dict(member=member), fields=['mode', 'billto', 'details'])[0]

billingpref_resource = BillingprefResource()
