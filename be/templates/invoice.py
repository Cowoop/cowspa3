import sphc
import sphc.more
import commonlib.helpers
import itertools
from operator import itemgetter

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
        container = tf.DIV()
        container.title = tf.DIV("I N V O I C E", id="invoice-header")

        container.top = tf.DIV(id="top")
        container.top.col1 = tf.DIV(id="top-col1")
        container.top.col2 = tf.DIV(id="top-col2")

        container.top.col1.sender = tf.DIV(id="issuer", Class="defs")
        if data.invoicepref.logo:
            container.top.col1.sender.logo = tf.DIV(tf.IMG(src=data.invoicepref.logo), Class="invoice-logo")
        container.top.col1.sender.title = tf.DIV(tf.H1(data.bizplace.name))

        container.top.col1.receiver = tf.DIV(id="receiver")
        container.top.col1.receiver.data = tf.TABLE(Class="defs")
        container.top.col1.receiver.data.caption = tf.CAPTION(data.member.display_name)
        container.top.col1.receiver.data.row = tf.TR([tf.TD("Membership No."),tf.TD(str(data.invoice.member))])

        container.top.col2.invoice = tf.DIV(id="invoice-details")
        container.top.col2.invoice.details = tf.TABLE(Class="defs")
        container.top.col2.invoice.details.row = tf.TR([tf.TD("Number"), tf.TD(str(data.invoice.id))])
        container.top.col2.invoice.details.date = tf.TR([tf.TD("Date"), tf.TD(data.invoice.created.strftime('%d %b %Y'))])
        container.top.col2.invoice.details.period = tf.TR([tf.TD("Period"),
            tf.TD(data.invoice.start_time.strftime('%d %b %Y')+" to "+data.invoice.end_time.strftime('%d %b %Y'))])
        if data.invoice.po_number:
            container.top.col2.invoice.details.po_number = tf.TR([tf.TD("P. O. Number"), tf.TD(data.invoice.po_number)])

        container.clear = sphc.more.clear()

        if data.invoice.notice:
            container.notice = tf.DIV(data.invoice.notice, Class="pre-wrap full box-bordered")

        usage_summary = tf.DIV()
        usages = tf.TABLE(id='usages_summary', Class="stripped")
        usages.caption = tf.h3("Usage Summary")
        usages.header = tf.TR()
        usages.header.cells = [tf.TH(name) for name in ('Resource', 'Amount')]
        for name, group in itertools.groupby(data.usages, itemgetter('resource_name')):
            usage_row = tf.TR()
            usage_row.td = tf.TD(name)
            usage_row.td = tf.TD(str(sum([usage.calculated_cost for usage in group])))
            usages.row = usage_row
        usage_row = tf.TR()
        usage_row.td = tf.TD("Sub Total")
        usage_row.td = tf.TD(str(data.invoice.cost))
        usages.row = usage_row
        usage_summary.table = usages
        container.usage_summary = usage_summary

        if data.invoicepref.terms_and_conditions:
            container.terms_and_conditions = tf.DIV()
            container.terms_and_conditions.heading = tf.H3("Terms & Conditions")
            container.terms_and_conditions.data = tf.DIV(data.invoicepref.terms_and_conditions)

        usage_details = tf.DIV()
        usages = tf.TABLE(id='usages_details', Class="stripped")
        usages.caption = tf.CAPTION("Usage Details")
        usages.header = tf.TR()
        usages.header.cells = [tf.TH(name) for name in ('Sr. No.', 'Resource', 'Rate', 'Quantity', 'Duration', 'Amount')]
        sr_no = 1
        for usage in data.usages:
            usage_row = tf.TR()
            usage_row.td = tf.TD(str(sr_no))
            usage_row.td = tf.TD(str(usage.resource_name))
            usage_row.td = tf.TD(str(usage.rate))
            usage_row.td = tf.TD(str(usage.quantity))
            usage_row.td = tf.TD(usage.start_time.strftime('%d %b %Y %I:%M%p')+" - "+usage.end_time.strftime('%d %b %Y %I:%M%p'))
            usage_row.td = tf.TD(str(usage.calculated_cost))
            usages.row = usage_row
            sr_no += 1
        usage_row = tf.TR()
        usage_row.td = tf.TD()
        usage_row.td = tf.TD()
        usage_row.td = tf.TD()
        usage_row.td = tf.TD()
        usage_row.td = tf.TH("Total")
        usage_row.td = tf.TD(str(data.invoice.cost))
        usages.row = usage_row
        usage_details.table = usages

        container.usage_details = usage_details

        if data.invoicepref.bank_details:
            container.bank_details = tf.DIV()
            container.bank_details.heading = tf.H3("Bank Details")
            container.bank_details.data = tf.DIV(data.invoicepref.bank_details)

        if data.invoicepref.due_date:
            container.payment_terms = tf.DIV()
            container.payment_terms.heading = tf.B("Payment Terms: ")
            container.payment_terms.data = tf.C("%s days" % data.invoicepref.due_date)

        return container
