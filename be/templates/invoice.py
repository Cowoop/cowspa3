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
    doc.body.top.sender.title = tf.H1("The Hub "+data.bizplace.name)
    
    doc.body.top.receiver = tf.DIV()
    doc.body.top.receiver.id = tf.DIV("Membership No. "+str(data.invoice.member))
    doc.body.top.receiver.member = tf.DIV(data.member.display_name)
    
    doc.body.top.invoice = tf.DIV("INVOICE")
    doc.body.top.invoice.id = tf.DIV("Number "+str(data.invoice.id))
    doc.body.top.invoice.date = tf.DIV("Date "+data.invoice.created.strftime('%d %b %Y'))
    doc.body.top.invoice.period = tf.DIV("Period "+data.invoice.start_time.strftime('%d %b %Y')+" to "+data.invoice.end_time.strftime('%d %b %Y'))
    
    usage_summary = tf.DIV()
    usages = tf.TABLE(id='usages_summary')
    usages.caption = tf.CAPTION("Usage Summary")
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
    
    usage_details = tf.DIV()
    usages = tf.TABLE(id='usages_details')
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
    usage_row.td = tf.TD("Total")
    usage_row.td = tf.TD(str(data.invoice.cost))
    usages.row = usage_row     
    usage_details.table = usages
    doc.body.usage_details = usage_details
    
    doc.body.bank_details = tf.DIV(data.bizplace.bank_details)
    return str(doc)
