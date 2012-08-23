import datetime
import sphc
import sphc.more
import commonlib.helpers
import itertools
import collections
import be.repository.access as dbaccess
from operator import itemgetter
from babel.numbers import get_currency_symbol, format_currency, format_number
odict = commonlib.helpers.odict
tf = sphc.TagFactory()

class Template(sphc.more.HTML5Page):
    jslibs = []
    css_links = []
    title = 'INVOICE'

    def style(self):
        return tf.STYLE(open('be/templates/css/invoice.css').read())

    def main(self):
        data = odict(self.data)
        currency = data.bizplace.currency
        locale = data.memberpref[0].language
        taxes_text = 'Inclusive of Taxes' if data.invoicepref.tax_included else 'Exclusive of Taxes'
        total_cost = sum(usage.cost for usage in data.usages)
        total_tax = sum(usage.tax_dict['total'] for usage in data.usages)
        date = data.invoice.sent or datetime.datetime.now()
        due_date = date + datetime.timedelta(data.invoicepref.due_date)

        address_lines = []
        address_items = ('address', 'city', 'province', 'country_label', 'pincode')
        for attr in address_items:
            v = data.billingpref.get(attr)
            if v: address_lines.append(v)

        def show_currency(num):
            return str(format_currency(num, currency, locale=locale))

        container = tf.DIV()
        container.title = tf.DIV("I N V O I C E", id="invoice-header")

        container.top = tf.DIV(id="top")
        container.top.col1 = tf.DIV(id="top-col1")
        container.top.col2 = tf.DIV(id="top-col2")

        container.top.col1.sender = tf.DIV(id="issuer", Class="defs")
        if not data.invoicepref.logo in ('data:', '', None):
            container.top.col1.sender.logo = tf.DIV(tf.IMG(src=data.invoicepref.logo, Class="invoice-logo"))
        else:
            container.top.col1.sender.title = tf.DIV(tf.H1(data.bizplace.name))

        container.top.col1.receiver = tf.DIV(id="receiver")
        container.top.col1.receiver.data = tf.TABLE(Class="defs")
        container.top.col1.receiver.data.caption = tf.CAPTION(data.billingpref['name'])
        container.top.col1.receiver.data.row = tf.TR([tf.TD("Membership No."),tf.TD(str(data.billingpref['number']))])

        container.top.col1.receiver.address = tf.ADDRESS('\n'.join(address_lines), Class='pre-wrap')
        #if data.billingpref['taxation_no']:
        #    container.top.col1.receiver.taxation_no = tf.DIV(tf.STRONG(data.billingpref['taxation_no']))

        container.top.col2.invoice = tf.DIV(id="invoice-details")
        container.top.col2.invoice.details = tf.TABLE(Class="defs")
        container.top.col2.invoice.details.row = tf.TR([tf.TD("Number"), tf.TD(str(data.invoice.number if data.invoice.number else "-"))])
        container.top.col2.invoice.details.period = tf.TR([tf.TD("Period"),
            tf.TD(commonlib.helpers.date4human(data.invoice.start_date)+" to "+commonlib.helpers.date4human(data.invoice.end_date))])
        container.top.col2.invoice.details.date = tf.TR([tf.TD("Date"), tf.TD(commonlib.helpers.date4human(date))])
        container.top.col2.invoice.details.date = tf.TR([tf.TD("Due Date"), tf.TD(commonlib.helpers.date4human(due_date))])
        if data.invoice.po_number:
            container.top.col2.invoice.details.po_number = tf.TR([tf.TD("P. O. Number"), tf.TD(data.invoice.po_number)])

        container.clear = sphc.more.clear()

        if data.invoice.notice:
            container.notice = tf.DIV()
            container.notice.header = tf.B('Note')
            container.notice.notice = tf.DIV(data.invoice.notice, Class="pre-wrap full box-bordered")
            container.notice.br = tf.BR()

        if data.invoicepref.freetext1:
            container.freetext1 = tf.DIV(data.invoicepref.freetext1, Class="pre-wrap full")

        usage_summary = tf.DIV()
        usages = tf.TABLE(id='usages_summary', Class="stripped")
        usages.caption = tf.h3("Usage Summary")
        usages.header = tf.THEAD()
        usages.header.cell = tf.TH('Description')
        usages.header.cell = tf.TH([('Amount (%s) ' % currency), tf.SPAN(taxes_text, Class='note')])
        usages.header.cell = tf.TH('Taxes (%s)' % currency)
        sorter = lambda usage: usage.resource_name
        for name, group in itertools.groupby(sorted(data.usages, key=sorter), itemgetter('resource_name')):
            group = list(group)
            row = tf.TR()
            row.td1 = tf.TD(name)
            row.td2 = tf.TD(format_number(sum([usage.cost for usage in group]), locale))
            row.td3 = tf.TD()
            #row.td3.tax = tf.DIV(format_number(sum(usage.tax_dict['total'] for usage in group)))
            tax_amount = collections.defaultdict(lambda: 0)
            tax_level = {}
            for usage in group:
                breakdown = usage.tax_dict['breakdown']
                for name, level, amount in breakdown:
                    tax_amount[name] += amount
                    tax_level[name] = level
            for (name, amount) in tax_amount.items():
                row.td3.taxline = tf.DIV('%s %s%%: %s' % (name, tax_level[name], format_number(amount, locale)))
            usages.row = row

        row = tf.TR()
        row.td1 = tf.TD("Sub Total")
        row.td2 = tf.TD(format_number(total_cost, locale))
        row.td3 = tf.TD(format_number(total_tax, locale))
        usages.row = row
        usage_summary.table = usages
        container.usage_summary = usage_summary

        table_headers = ['Sr. no.', 'Resource', 'Quantity', 'Duration', 'Amount (%s)' % currency]
        multimember_invoice = False
        members = set(usage.member for usage in data.usages)
        if members != set([data.member.id]):
            table_headers.insert(1, 'Member')
            multimember_invoice = True
        usage_details = tf.DIV()
        usages = tf.TABLE(id='usages_details', Class="stripped pagefix")
        usages.caption = tf.CAPTION("Usage Details")
        usages.header = tf.THEAD()
        usages.header.cells = [tf.TH(name) for name in table_headers]
        sr_no = 1
        for usage in data.usages:
            usage_row = tf.TR()
            usage_row.td = tf.TD(str(sr_no))
            if multimember_invoice: usage_row.td = tf.TD(dbaccess.member_store.get(usage.member, "name"))
            usage_row.td = tf.TD(usage.resource_name)
            usage_row.td = tf.TD(str(usage.quantity))
            usage_row.td = tf.TD(commonlib.helpers.datetime4human(usage.start_time)+" - "+commonlib.helpers.datetime4human(usage.end_time))
            usage_row.td = tf.TD(format_number(usage.cost, locale))
            usages.row = usage_row
            sr_no += 1

        if not data.invoicepref.tax_included:
            usage_row = tf.TR()
            usage_row.td = tf.TD()
            if multimember_invoice: usage_row.td = tf.TD()
            usage_row.td = tf.TD()
            usage_row.td = tf.TD()
            usage_row.td = tf.TH("Taxes")
            usage_row.td = tf.TD(format_number(total_tax, locale))
            usages.row = usage_row

        usage_row = tf.TR()
        usage_row.td = tf.TD()
        if multimember_invoice: usage_row.td = tf.TD()
        usage_row.td = tf.TD()
        usage_row.td = tf.TD()
        usage_row.td = tf.TH("Total")
        usage_row.td = tf.TD(format_number(data.invoice.total, locale))
        usages.row = usage_row
        usage_details.table = usages

        container.usage_details = usage_details

        if data.invoicepref.freetext2:
            container.notice = tf.DIV(data.invoicepref.freetext2, Class="pre-wrap full")

        if data.invoicepref.bank_details:
            container.bank_details = tf.DIV()
            container.bank_details.heading = tf.H3("Bank Details")
            container.bank_details.data = tf.DIV(data.invoicepref.bank_details, Class="pre-wrap")

        container.payment_terms = tf.DIV()
        container.payment_terms.heading = tf.H3("Payment Terms")
        container.payment_terms.data = tf.C(data.invoicepref.payment_terms, Class="pre-wrap")
        container.payment_terms.br = tf.BR()

        footer_items = [data.invoicepref.company_no, data.bizplace.website, data.bizplace.phone]
        footer = ' | '.join(item for item in footer_items if item)
        container.nl = tf.BR()
        container.footer = tf.DIV(footer, Class='footer')

        container.jquery = sphc.more.script_fromfile('be/templates/jquery-1.7.1.min.js')
        container.script = sphc.more.script_fromfile("be/templates/pagefix.js")

        return container
