import sphc
import commonlib.helpers

odict = commonlib.helpers.odict
tf = sphc.TagFactory()

def template(data):
    data = odict(**data)
    doc = tf.HTML()
    doc.style = tf.STYLE(open('invoice.css').read())
    doc.body = tf.BODY()
    doc.body.top = tf.DIV()
    doc.body.top.sender = tf.DIV()
    doc.body.top.sender.title = tf.H1(data.sender_title)
    return str(doc)
