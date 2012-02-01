import datetime
import be.repository.access as dbaccess
import be.apis.activities as activitylib
import be.apis.member as memberlib
import commonlib.helpers

member_store = dbaccess.stores.member_store
invoicepref_store = dbaccess.stores.invoicepref_store

modes = commonlib.helpers.odict(self=0, custom=1, other=2)

class BillingprefResource:

    def update(self, member, **mod_data):

        if mod_data['mode'] == modes.other and mod_data['billto'] == member:
            mod_data['mode'] = modes.self
            mod_data['billto'] = None
        invoicepref_store.update_by(dict(owner=member), **mod_data)

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

        return details

    def info(self, member):
        return invoicepref_store.get_by(dict(owner=member), fields=['mode', 'billto', 'details'])[0]

    def get_dependent_members(self, member):
        """
        returns list of members whose biiling is forwarded to specified member
        """
        return dbaccess.get_billing_dependent_members(member)

billingpref_resource = BillingprefResource()
