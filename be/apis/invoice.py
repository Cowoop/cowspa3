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
import be.apis.messagecust as messagecustlib

invoice_store = dbaccess.stores.invoice_store
usage_store = dbaccess.stores.usage_store
member_store = dbaccess.stores.member_store
bizplace_store = dbaccess.stores.bizplace_store
invoicepref_store = dbaccess.stores.invoicepref_store
memberpref_store = dbaccess.stores.memberpref_store

invoice_storage_dir = "be/repository/invoices/"

def create_invoice_pdf(invoice_id):
    invoice = invoice_store.get(invoice_id)
    usages = usage_store.get_many(invoice.usages)
    bizplace = bizplace_store.get(invoice.issuer)
    member = member_store.get(invoice.member)
    memberpref = memberpref_store.get_by(dict(member=invoice.member))
    invoicepref = invoicepreflib.invoicepref_resource.info(invoice.issuer)
    data = dict(invoice=invoice, usages=usages, bizplace=bizplace,
            member=member, invoicepref=invoicepref, memberpref=memberpref)
    html_path = invoice_storage_dir + str(invoice_id) + '.html'
    be.templates.invoice.Template(data).write(html_path)
    if invoice['number']:
        pdf_path = invoice_storage_dir + str(invoice_id) + '.pdf'
        pdf = commonlib.helpers.html2pdf(html_path, pdf_path)
    return True


class InvoiceCollection:

    def new(self, issuer, member, po_number, start_date, end_date, notice='', usages=[], new_usages=[], state=0, number=None):
        """
        usages --> The list of existing usage_ids
        new_usages --> The list of usage data which needs to create
        """
        for usage in new_usages:
            usage['member'] = member
            usages.append(usagelib.usage_collection.new(**usage))

        created = datetime.datetime.now()
        cost = decimal.Decimal(sum([usagelib.usage_resource.get(usage, 'cost') for usage in usages]))
        data = dict(issuer=issuer, member=member, usages=usages, sent=None, cost=cost, tax_dict={}, start_date=start_date, end_date=end_date, state=state, created=created, notice=notice, po_number=po_number)
        if number: data['number'] = number
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
        if invoice_store.get(invoice_id, 'sent'):
            msg = "You can not delete sent invoice."
            raise Exception(msg)
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
        return invoice_store.get_by(crit, fields=['number', 'cost', 'created', 'sent', 'id'], hashrows=hashrows)

class InvoiceResource:

    def update(self, invoice_id, **mod_data):
        """
        """
        invoice_store.update(invoice_id, **mod_data)
        if 'usages' in mod_data:
            old_usages = invoice_store.get(invoice_id, ['usages'])
            mod_data = dict(invoice=None)
            usage_store.update_many(old_usages, **mod_data)

            new_usages = mod_data['usages']
            mod_data = dict(invoice=invoice_id)
            usage_store.update_many(new_usages, **mod_data)
        return True

    def send(self, invoice_id, mailtext=None):
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
        if not invoice_store.get(invoice_id, 'number'):
            dbaccess.update_invoice_number(invoice_id, invoice['issuer'], invoicing_pref['start_number'])
            create_invoice_pdf(invoice_id)
        member = access.stores.member_store.get(member_id, ['first_name', 'last_name', 'name', 'number', 'email'])
        billingpref = billingpreflib.billingpref_resource.get_details(invoice_id)
        data = dict(LOCATION_PHONE=billingpref.phone, LOCATION=issuer.name, MEMBER_FIRST_NAME=member.first_name, MEMBER_LAST_NAME=member.last_name, MEMBERSHIP_NUMBER=member.number, MEMBER_EMAIL=member.email, HOSTS_EMAIL=issuer.host_email, LOCATION_URL=issuer.url, CURRENCY=issuer.currency)
        mcust = mailtext or messagecustlib.get(issuer.id, 'invoice_mail')
        text = string.Template(mcust.content).substitute(**data)
        env.mailer.send(issuer.email, email, subject=subject, rich=text, plain='', cc=[], bcc=bcc, attachment=attachment)
        return self.update(invoice_id, sent=datetime.datetime.now())

    def get(self, invoice_id, attr):
        return invoice_store.get(invoice_id, attr)

invoice_collection = InvoiceCollection()
invoice_resource = InvoiceResource()
