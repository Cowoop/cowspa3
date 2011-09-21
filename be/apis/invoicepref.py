import datetime
import be.repository.access as dbaccess
import be.apis.activities as activitylib

member_store = dbaccess.stores.member_store
invoicepref_store = dbaccess.stores.invoicepref_store
bizplace_store = dbaccess.stores.bizplace_store
memberpref_store = dbaccess.stores.memberpref_store

class InvoiceprefCollection:
    def new(self, owner, email_text="", terms_and_conditions="", due_date=15, bcc_email="", bank_details=""):

        data = dict(owner=bizplace_store.ref(owner), email_text=email_text, terms_and_conditions=terms_and_conditions, due_date=due_date, bcc_email=bcc_email, bank_details=bank_details)
      
        invoicepref_store.add(**data)

        return True
        
class InvoiceprefResource:

    def update(self, owner, **mod_data):
        invoicepref_store.update_by(dict(owner=bizplace_store.ref(owner)), **mod_data)
        return True

    def info(self, owner):
        return invoicepref_store.get_by(dict(owner=bizplace_store.ref(owner)), ['email_text', 'terms_and_conditions', 'due_date', 'bcc_email', 'bank_details', 'logo'])[0]
        
    def get(self, owner, attrname):
        return invoicepref_store.get_by(dict(owner=bizplace_store.ref(owner)), fields=[attrname])[0][attrname]

    def set(self, owner, attrname, v):
        self.update(owner, **{attrname: v})
        return True

invoicepref_resource = InvoiceprefResource()
invoicepref_collection = InvoiceprefCollection()
