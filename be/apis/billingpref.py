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
                details = member_store.get(billto, ['name', 'address', 'city', 'province', 'country', 'pincode', 'phone', 'email'])
                break
            elif mode == modes.custom:
                break
            elif mode == modes.other:
                continue

        details['number'] = member_store.get((billto or member), ['number'])
        return details

    def info(self, member):
        result = invoicepref_store.get_by(dict(owner=member), fields=['mode', 'taxation_no', 'billto', 'details', 'tax_exemptions_at'])[0]
        if result.tax_exemptions_at == None:
            result['tax_exemptions_at'] = []
        return result

    def get_dependent_members(self, member):
        """
        returns list of members whose biiling is forwarded to specified member
        """
        return dbaccess.get_billing_dependent_members(member)

    def set_tax_exemption(self, member, tax_exemption_at, applicable):
        """
        applicable: True/False
        """
        tax_exemptions_at = invoicepref_store.get_by({'owner':member}, fields=['tax_exemptions_at'])[0].tax_exemptions_at or []
        exemption_now = tax_exemption_at in tax_exemptions_at
        changed = False
        if applicable == False and exemption_now:
            tax_exemptions_at.remove(tax_exemption_at)
            changed = True
        elif applicable == True and not exemption_now:
            tax_exemptions_at.append(tax_exemption_at)
            changed = True
        if changed:
            mod_data = dict(tax_exemptions_at=tax_exemptions_at)
            invoicepref_store.update_by(dict(owner=member), **mod_data)


billingpref_resource = BillingprefResource()
