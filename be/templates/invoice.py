import sphc
import commonlib.helpers
import itertools
from operator import itemgetter

odict = commonlib.helpers.odict
tf = sphc.TagFactory()

def template(data):
    data = odict(**data)
    doc = tf.HTML()
    #doc.style = tf.STYLE(open('invoice.css').read())
    doc.body = tf.BODY()
    
    doc.body.top = tf.DIV()
    doc.body.top.sender = tf.DIV()
    doc.body.top.sender.logo = tf.IMG(src=data.invoicepref.logo, width="100", height="100")
    doc.body.top.sender.title = tf.H1("The Hub "+data.bizplace.name)
    
    doc.body.top.receiver = tf.DIV()
    doc.body.top.receiver.id = tf.DIV()
    doc.body.top.receiver.id.label = tf.H3("Membership No. ")
    doc.body.top.receiver.id.number = tf.H4(str(data.invoice.member))
    doc.body.top.receiver.dname = tf.DIV()
    doc.body.top.receiver.dname.data = tf.H4(data.member.display_name)
    
    doc.body.top.invoice = tf.DIV()
    doc.body.top.invoice.heading = tf.H3("INVOICE")
    doc.body.top.invoice.list = tf.DL()
    doc.body.top.invoice.list.id = tf.DT()
    doc.body.top.invoice.list.id.heading = tf.H4("Number")
    doc.body.top.invoice.list.data = tf.DD(str(data.invoice.id))
    doc.body.top.invoice.list.date = tf.DT()
    doc.body.top.invoice.list.date.heading = tf.H4("Date")
    doc.body.top.invoice.list.data = tf.DD(data.invoice.created.strftime('%d %b %Y'))
    doc.body.top.invoice.list.period = tf.DT()
    doc.body.top.invoice.list.period.heading = tf.H4("Period")
    doc.body.top.invoice.list.data = tf.DD(data.invoice.start_time.strftime('%d %b %Y')+" to "+data.invoice.end_time.strftime('%d %b %Y'))
    
    doc.body.notice = tf.DIV()
    doc.body.notice.heading = tf.H3("Notice")
    doc.body.notice.data = tf.DIV(data.invoice.notice)
    
    usage_summary = tf.DIV()
    usages = tf.TABLE(id='usages_summary')
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
    doc.body.usage_summary = usage_summary
    
    doc.body.terms_and_conditions = tf.DIV()
    doc.body.terms_and_conditions.heading = tf.H3("Terms & Conditions")
    doc.body.terms_and_conditions.data = tf.DIV(data.invoicepref.terms_and_conditions)
    
    usage_details = tf.DIV()
    usages = tf.TABLE(id='usages_details')
    usages.caption = tf.H3("Usage Details")
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
    doc.body.usage_details = usage_details
    
    doc.body.bank_details = tf.DIV()
    doc.body.bank_details.heading = tf.H3("Bank Details")
    doc.body.bank_details.data = tf.DIV(data.invoicepref.bank_details)
    
    doc.body.payment_terms = tf.DIV()
    doc.body.payment_terms.heading = tf.H3("Payment Terms")
    doc.body.payment_terms.data = tf.DIV("%sdays" % data.invoicepref.due_date)
    
    return str(doc)
