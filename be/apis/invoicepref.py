import datetime
import be.repository.access as dbaccess
import be.apis.activities as activitylib
import commonlib.helpers

bizplace_store = dbaccess.stores.bizplace_store
member_store = dbaccess.stores.member_store
invoicepref_store = dbaccess.stores.invoicepref_store
memberpref_store = dbaccess.stores.memberpref_store
modes = commonlib.helpers.odict(**{'self':0, 'custom':1, 'another':2, 'organization':3})

class InvoiceprefCollection:
    def new(self, owner, start_number=None, payment_terms="", due_date=15, bcc_email="", bank_details="", mode=modes.self, freetext1='', freetext2='', billto=None, details=None, company_no=None):

        data = dict(owner=owner, payment_terms=payment_terms, due_date=due_date, bcc_email=bcc_email, bank_details=bank_details, start_number=start_number, mode=mode, freetext1=freetext1, freetext2=freetext2, billto=billto, details=details, company_no=company_no)

        invoicepref_store.add(**data)

        return True

class InvoiceprefResource:

    def update(self, owner, **mod_data):
        invoicepref_store.update_by(dict(owner=owner), **mod_data)

        bizplace_name = bizplace_store.get(owner, fields=['name'])
        data = dict(name=bizplace_name, attrs=', '.join(attr for attr in mod_data))
        activity_id = activitylib.add('invoicepref_management', 'invoicepref_updated', data)
        return True

    def info(self, owner):
        fields = ['company_no', 'payment_terms', 'due_date', 'bcc_email', 'bank_details', 'logo', 'tax_included', 'freetext1', 'freetext2', 'email_text']
        return invoicepref_store.get_by(dict(owner=owner), fields)[0]

    def get(self, owner, attrname):
        return invoicepref_store.get_by(dict(owner=owner), fields=[attrname])[0][attrname]

    def set(self, owner, attrname, v):
        self.update(owner, **{attrname: v})
        return True

    def get_taxinfo(self, owner):
        d = invoicepref_store.get_by(dict(owner=owner), fields=['tax_included', 'taxes'])[0]
        taxes = dict((k, float(v)) for k,v in d['taxes'].items()) if d['taxes'] else d['taxes']
        return dict(taxes=taxes, tax_included=d['tax_included'])

invoicepref_resource = InvoiceprefResource()
invoicepref_collection = InvoiceprefCollection()
