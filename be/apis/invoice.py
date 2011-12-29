import datetime
import decimal
import be.repository.access as dbaccess
import be.apis.usage as usagelib
import be.templates.invoice
import operator
import os
import commonlib.helpers
import be.apis.activities as activitylib
import be.apis.invoicepref as invoicepreflib
import be.apis.billingpref as billingpreflib

invoice_store = dbaccess.stores.invoice_store
usage_store = dbaccess.stores.usage_store
member_store = dbaccess.stores.member_store
bizplace_store = dbaccess.stores.bizplace_store
invoicepref_store = dbaccess.stores.invoicepref_store
memberpref_store = dbaccess.stores.memberpref_store

def create_invoice_pdf(invoice_id):
    invoice = invoice_store.get(invoice_id)
    usages = usage_store.get_many(invoice.usages)
    bizplace = bizplace_store.get(invoice.issuer)
    member = member_store.get(invoice.member)
    memberpref = memberpref_store.get_by(dict(member=invoice.member))
    invoicepref = invoicepreflib.invoicepref_resource.info(invoice.issuer)
    data = dict(invoice=invoice, usages=usages, bizplace=bizplace,
            member=member, invoicepref=invoicepref, memberpref=memberpref)
    html_path = '%sinvoice_%s.html' % ("be/repository/invoices/", invoice_id)
    pdf_path = '%sinvoice_%s.pdf' % ("be/repository/invoices/", invoice_id)
    be.templates.invoice.Template(data).write(html_path)
    pdf = commonlib.helpers.html2pdf(html_path, pdf_path)
    return pdf


class InvoiceCollection:

    def new(self, issuer, member, po_number, start_date, end_date, notice, usages=[], new_usages=[], state=0):
        """
        usages --> The list of existing usage_ids
        new_usages --> The list of usage data which needs to create
        """
        for usage in new_usages:
            usage['member'] = member
            usages.append(usagelib.usage_collection.new(**usage))

        created = datetime.datetime.now()
        cost = decimal.Decimal(sum([usagelib.usage_resource.get(usage, 'cost') for usage in usages]))
        number = dbaccess.generate_invoice_number(issuer)
        data = dict(issuer=issuer, member=member, usages=usages, number=number, sent=None, cost=cost, tax_dict={}, start_date=start_date, end_date=end_date, state=state, created=created, notice=notice, po_number=po_number)
        invoice_id = invoice_store.add(**data)

        mod_data = dict(invoice=invoice_id)
        usage_store.update_many(usages, **mod_data)

        data = dict(name=member_store.get(member, ['name']), issuer=bizplace_store.get(issuer, ['name']), invoice_id=invoice_id, member_id=member)
        activity_id = activitylib.add('invoice_management', 'invoice_created', data, created)
        
        create_invoice_pdf(invoice_id)
        
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
        query_parts = q.split()
        return dbaccess.search_invoice(query_parts, options, limit)

    def list(self, issuer, limit=100):
        data = dict(issuer=issuer, limit=limit)
        return dbaccess.list_invoices(**data)
    
    def by_member(self, issuer, member, hashrows=True):
        crit = dict(issuer=issuer, member=member)
        return invoice_store.get_by(crit, fields=['number', 'cost', 'created', 'id'], hashrows=hashrows)

class InvoiceResource:

    def update(self, invoice_id, **mod_data):
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
        invoice = invoice_store.get(invoice_id, ['member', 'issuer'])
        member_id = invoice['member']
        invoicing_pref = invoicepref_store.get_by(dict(owner=invoice.issuer))[0]
        issuer = bizplace_store.get(invoice['issuer'])
        email = billingpreflib.billingpref_resource.get_details(member=member_id)['email']
        subject = issuer.name + ' | Invoice'
        attachment = os.getcwd() + '/be/repository/invoices/invoice_' + str(invoice_id) + '.pdf'
        bcc = [invoicing_pref.bcc_email] if invoicing_pref.bcc_email else []
        env.mailer.send(issuer.email, email, subject=subject, rich=invoicing_pref.email_text, \
            plain='', cc=[], bcc=bcc, attachment=attachment)
        return self.update(invoice_id, sent=datetime.datetime.now())

invoice_collection = InvoiceCollection()
invoice_resource = InvoiceResource()
