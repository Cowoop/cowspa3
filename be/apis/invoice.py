import datetime
import be.repository.access as dbaccess
import operator

invoice_store = dbaccess.stores.invoice_store
usage_store = dbaccess.stores.usage_store
member_store = dbaccess.stores.member_store

class InvoiceCollection:

    def new(self, member, usages, state=0, number=None, sent=None, invoicee_details=None, cost=None, tax_dict=None):
        """
        """
        usage_periods = usage_store.get_many(usages, ['start_time', 'end_time'])
        start_time = min(usage_periods, key=operator.itemgetter('start_time'))['start_time']
        end_time = max(usage_periods, key=operator.itemgetter('end_time'))['end_time']

        created = datetime.datetime.now()
        data = dict(member=member, usages=usages, number=number, sent=sent, invoicee_details=invoicee_details, cost=cost, tax_dict=tax_dict, start_time=start_time, end_time=end_time, state=state, created=created)
        invoice_id = invoice_store.add(**data)

        mod_data = dict(invoice=invoice_id)
        usage_store.update_many(usages, **mod_data)

        return invoice_id

    def delete(self, invoice_id):
        """
        Delete Invoice
        """
        if invoice_store.remove(invoice_id):

            mod_data = dict(invoice=None)
            usage_ids = usage_store.get_by(dict(invoice=invoice_id), ['id'])
            usages = []
            for usage_id in usage_ids:
                usages.append(usage_id['id'])
            return usage_store.update_many(tuple(usages), **mod_data)

        return False
        
    def search(self, q, options={'mybizplace': False}, limit=5):
        """
        q: id OR first name or last name or both of invoicee.
        limit: number of results to return
        return -> list of tuples containing invoice id and member id
        """
        keys = q.split()
        return dbaccess.search_invoice(keys, options, limit)


class InvoiceResource:

    def update(self, invoice_id, mod_data):
        """
        """
        invoice_store.update(invoice_id, **mod_data)
        if 'usages' in mod_data:
            old_usages = invoice_store.get(invoice_id, ['usages'])
            modf_data = dict(invoice=None)
            usage_store.update_many(old_usages, **modf_data)

            new_usages = mod_data['usages']
            modf_data = dict(invoice=invoice_id)
            usage_store.update_many(new_usages, **modf_data)
        return True

    def send(self, invoice_id):
        """
        """
        member = invoice_store.get(invoice_id, ['member'])
        email = member_store.get(member, ['email'])
        env.mailer.send(email, subject='Invoice Details', rich='<b>See the attached Pdf.</b>', plain='', cc=[], bcc=[], attachment='')

invoice_collection = InvoiceCollection()
invoice_resource = InvoiceResource()
