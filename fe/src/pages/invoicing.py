import sphc
import sphc.more
import fe.bases

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

class New(BasePage):

    title = "New Invoice"

    def content(self):
        container = tf.DIV()

        container.member_field = tf.INPUT(type="text", name="invoicee", placeholder="invoicee")
        container.member_info = tf.DIV(Class="invoicee-info")
        container.po_number = tf.DIV()
        container.po_number.label = tf.LABEL("P. O. Number", For="po_number")
        container.po_number.input = tf.INPUT(type="text", name="po_number", placeholder="Purchase Order number")
        container.notice = tf.LABEL("Notice/Annoucement (only for this invoice)")

        return container
