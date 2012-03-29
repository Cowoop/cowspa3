import datetime
import decimal
import be.repository.access as dbaccess
import be.apis.usage as usagelib
import be.templates.invoice
import be.errors as errors
import operator
import os
import commonlib.helpers
import be.apis.activities as activitylib
import be.apis.invoicepref as invoicepreflib
import be.apis.billingpref as billingpreflib
import be.apis.messagecust as messagecustlib
import be.apis.pricing as pricinglib

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
    billingpref = billingpreflib.billingpref_resource.get_details(invoice.member)
    data = dict(invoice=invoice, usages=usages, bizplace=bizplace, billingpref=billingpref,
            member=member, invoicepref=invoicepref, memberpref=memberpref)
    html_path = invoice_storage_dir + str(invoice_id) + '.html'
    be.templates.invoice.Template(data).write(html_path)
    if invoice['number']:
        pdf_path = invoice_storage_dir + str(invoice_id) + '.pdf'
        pdf = commonlib.helpers.html2pdf(html_path, pdf_path)
    return True


class InvoiceCollection:

    def new(self, issuer, member, po_number=None, start_date=None, end_date=None, notice='', usages=[], new_usages=[], state=0):
        """
        usages --> The list of existing usage_ids
        new_usages --> The list of usage data which needs to create
        """
        for usage in new_usages:
            usage['member'] = member
            usages.append(usagelib.usage_collection.new(**usage))

        created = datetime.datetime.now()
        usages_linked = usage_store.get_many(usages, ['id', 'resource_id', 'member', 'quantity', 'cost', 'start_time', 'end_time', 'tax_dict', 'total'])

        # safe guard
        tax_exemption_applicable = issuer in (invoicepref_store.get_by({'owner':member}, fields=['tax_exemptions_at'])[0].tax_exemptions_at or [])
        usages_updated = False
        for usage in usages_linked:
            if (None in (usage.total, usage.cost)) or (tax_exemption_applicable and usage.tax_dict['total']):
                usagelib.usage_resource.update(usage.id, recalculate=True)
                usages_updated = True
        usages_linked = usage_store.get_many(usages, ['id', 'resource_id', 'member', 'quantity', 'cost', 'start_time', 'end_time', 'total'])

        # below test does not take billto settings in account hence commenting out for now
        #if not all((usage.member == member) for usage in usages_linked):
        #    msg = "One of the usages %s does not have member_id matching %s" % (str(usages), member)
        #    raise Exception(msg)

        total = decimal.Decimal(sum(usage.total for usage in usages_linked))
        start_date = start_date or min(usage.start_time.date() for usage in usages_linked)
        end_date = end_date or min((usage.end_time or usage.start_time).date() for usage in usages_linked)
        data = dict(issuer=issuer, member=member, usages=usages, sent=None, total=total, tax_dict={}, start_date=start_date, end_date=end_date, state=state, created=created, notice=notice, po_number=po_number)
        invoice_id = invoice_store.add(**data)

        mod_data = dict(invoice=invoice_id)
        usage_store.update_many(usages, **mod_data)

        data = dict(name=member_store.get(member, ['name']), issuer=bizplace_store.get(issuer, ['name']), invoice_id=invoice_id, member_id=member)
        activity_id = activitylib.add('invoice_management', 'invoice_created', data, created)

        create_invoice_pdf(invoice_id)

        return invoice_id

    def m_new(self, issuer, member, po_number, start_date, end_date, created, total, sent=None, notice='', usages=[], new_usages=[], state=0, number=None):
        for usage in new_usages:
            usage['member'] = member
            usages.append(usagelib.usage_collection.new(**usage))

        created = datetime.datetime.now()
        data = dict(issuer=issuer, member=member, usages=usages, sent=sent, total=total, tax_dict={}, start_date=start_date, end_date=end_date, state=state, created=created, notice=notice, po_number=po_number)
        if number: data['number'] = number

        invoice_id = invoice_store.add(**data)

        mod_data = dict(invoice=invoice_id)
        usage_store.update_many(usages, **mod_data)

        data = dict(name=member_store.get(member, ['name']), issuer=bizplace_store.get(issuer, ['name']), invoice_id=invoice_id, member_id=member)
        activity_id = activitylib.add('invoice_management', 'invoice_created', data, created)

        return invoice_id

    def generate(self, issuer, member, usages_before):
        usages = usagelib.usage_collection.uninvoiced(member_id=member, res_owner_id=issuer, start=usages_before, end=None)
        return self.new(issuer, member, start_date=None, end_date=None, usages=[usage.id for usage in usages])

    def delete(self, invoice_id, force=False):
        """
        Delete Invoice
        """
        if invoice_store.get(invoice_id, 'sent') and not force:
            msg = "You can not delete sent invoice."
            raise errors.ErrorWithHint(msg)

        if invoice_store.remove(invoice_id):
            mod_data = dict(invoice=None)
            usage_ids = tuple(row[0] for row in usage_store.get_by(dict(invoice=invoice_id), ['id'], hashrows=False))
            return usage_store.update_many(usage_ids, **mod_data)

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
        """
        limit: -1 is no limit
        returns list of invoice dicts
        """
        data = dict(issuer=issuer, limit=limit)
        return dbaccess.list_invoices(**data)

    def by_member(self, issuer, member, hashrows=True):
        crit = dict(issuer=issuer, member=member)
        return invoice_store.get_by(crit, fields=['number', 'total', 'created', 'sent', 'id'], hashrows=hashrows)

    def unsent(self, issuer):
        """
        list of unsent invoices
        """
        crit = dict(issuer=issuer)
        unsent = invoice_store.get_by(crit, fields=['id', 'member', 'total', 'created'])
        members = dict(member_store.get_many([invoice.member for invoice in unsent], fields=['id', 'name'], hashrows=False))
        for invoice in unsent:
            invoice['member_name'] = members[invoice.member]
        return unsent

class InvoiceResource:

    def info(self, invoice_id):
        return invoice_store.get(invoice_id, ['id', 'number', 'sent', 'member', 'issuer', 'total', 'created', 'usages'])

    def update(self, invoice_id, **mod_data):
        """
        """
        invoice = invoice_store.get(invoice_id)

        if invoice.sent:
            msg = "You can not modify sent invoice."
            raise Exception(msg)

        if 'usages' in mod_data:
            old_usages = invoice.usages
            mod_data = dict(invoice=None)
            usage_store.update_many(old_usages, **mod_data)

            new_usages = mod_data['usages']
            mod_data = dict(invoice=invoice_id)
            usage_store.update_many(new_usages, **mod_data)

            mod_data['total'] = decimal.Decimal(sum([row[0] for row in usagelib.usage_resource.get_many(new_usages, 'amount', False)]))

        invoice_store.update(invoice_id, **mod_data)
        return True

    def send(self, invoice_id, mailtext=None):
        """
        """
        invoice = invoice_store.get(invoice_id, ['member', 'issuer', 'number'])
        member_id = invoice['member']
        invoicing_pref = invoicepref_store.get_by(dict(owner=invoice.issuer))[0]
        issuer = bizplace_store.get(invoice['issuer'])
        member = dbaccess.member_store.get(member_id, ['first_name', 'last_name', 'name', 'number', 'email', 'website'])
        if not invoice.number:
            dbaccess.number_a_invoice(invoice_id, invoice['issuer'], invoicing_pref['start_number'])
            create_invoice_pdf(invoice_id)
        invoice = invoice_store.get(invoice_id, ['member', 'issuer', 'number'])
        email = billingpreflib.billingpref_resource.get_details(member=member_id)['email'] or member.email
        subject = issuer.name + ' | Invoice ' + str(invoice.number)
        attachment = ((invoice_storage_dir + str(invoice_id) + '.pdf'), "invoice-%s.pdf" % invoice.number)
        bcc = invoicing_pref.bcc_email if invoicing_pref.bcc_email else None
        if bcc and ',' in bcc: # we have multiple email addresses
            bcc = bcc.split(',')[:2] # max 2
        data = dict(LOCATION_PHONE=issuer.phone, LOCATION=issuer.name, MEMBER_FIRST_NAME=member.first_name, MEMBER_LAST_NAME=member.last_name, MEMBERSHIP_NUMBER=member.number, MEMBER_EMAIL=email, HOSTS_EMAIL=issuer.host_email or issuer.email, LOCATION_URL=issuer.website or '', CURRENCY=issuer.currency)
        mailtext = mailtext or messagecustlib.get(issuer.id, 'invoice')
        notification = commonlib.messaging.messages.invoice(data, overrides=dict(plain=mailtext, bcc=bcc, attachment=attachment))
        notification.build()
        notification.email()
        return True

    def get(self, invoice_id, attr):
        return invoice_store.get(invoice_id, attr)

invoice_collection = InvoiceCollection()
invoice_resource = InvoiceResource()
