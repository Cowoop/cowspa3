import sphc
import sphc.more
import fe.bases

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

class New(BasePage):

    title = "New Invoice"

    def content(self):
        container = tf.DIV()

        container.member_field = tf.INPUT(type="text", name="invoicee", placeholder="Invoicee")
        container.member_info = tf.DIV(Class="invoicee-info")
        container.po_number = tf.DIV()
        container.po_number.label = tf.LABEL("P. O. Number", For="po_number")
        container.po_number.input = tf.INPUT(type="text", name="po_number", placeholder="Purchase Order number")
        container.notice = tf.DIV()
        container.notice.label = tf.LABEL("Notice/Annoucement (only for this invoice)")
        container.notice.text = tf.TEXTAREA(name="message")

        usages = tf.TABLE()
        usages.caption = tf.CAPTION("Usages")
        usages.header = tf.TR()
        usages.header.cells = [tf.TH(name) for name in ('Resource', 'Rate', 'Qty', 'Unit', 'Start-End', 'Total', 'Actions')]

        usage_tmpl = tf.TR()
        usage_tmpl.td = tf.TD('${resource_name}')
        usage_tmpl.td = tf.TD('${rate}')
        usage_tmpl.td = tf.TD('${qty}')
        usage_tmpl.td = tf.TD('${unit}')
        usage_tmpl.td = tf.TD('${start}')
        usage_tmpl.td = tf.TD('${end}')
        usage_tmpl.td = tf.TD('${total}')

        add_usage_form = sphc.more.VForm(id='new-usage-form')
        add_usage_form.add_field("Resource Name", tf.INPUT(name='resource_name', id='resource_name', nv_attrs=('required',), placeholder="Resource name"))
        add_usage_form.add_field("Rate", tf.INPUT(name='name', id='name', nv_attrs=('required',), placeholder="eg. 12.00"), "Do not include currency")
        add_usage_form.add_field("Quantity", tf.INPUT(name='quantity', id='quantity', nv_attrs=('required',), placeholder="eg. 10. Not applicable for time based resource"), fhelp="For non time based resources. Do not include unit")
        add_usage_form.add_field("Start", tf.INPUT(name='start', id='start', nv_attrs=('required',)))
        add_usage_form.add_field("End", tf.INPUT(name='end', id='end'), "Optional. Only for time based resources.")
        add_usage_section = tf.DIV(id='new-usage-section', Class='hidden')
        add_usage_section.form = add_usage_form.build()

        new = tf.BUTTON("Add usage", id="new-usage-button")
        script = tf.SCRIPT("""
        $('#new-usage-form #start').datetimepicker({
            timeFormat: 'h:m',
            dateFormat: 'dd.mm.yy',
        });
        $('#new-usage-form #end').datetimepicker({
            timeFormat: 'h:m',
        });
        $('#new-usage-button').click(function() {
            $('#new-usage-form').dialog({ title: "Create new usage", width: 500});
        });
        """)

        container.usages = usages
        container.new = new
        container.form = add_usage_section
        container.script = script

        return container
