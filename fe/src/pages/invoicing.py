# -*- coding: UTF-8 -*-
import sphc
import sphc.more
import fe.bases

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

class InvoiceBasePage(BasePage):
    def search(self):
        row = tf.DIV(Class="searchbox")
        cell = tf.DIV()
        cell.data = tf.SPAN("Invoice Search", Class="search-label", For="search")
        row.cell = cell
        cell = tf.DIV()
        cell.data = tf.INPUT(id="search", Class="search-input", type="text")
        row.cell = cell
        return row

class New(BasePage):

    title = "New Invoice"
    current_nav = 'Invoicing'

    def content(self):
        container = tf.DIV(id='invoice-form-container')
        container.header = tf.DIV("INVOICE", id="invoice-header")
        content = tf.DIV(id='invoice-content')
        container.content = content

        content.col1 = tf.DIV(id='col1')
        content.col2 = tf.DIV(id='col2')

        content.col1.member_field = tf.INPUT(type="text", name="invoicee", id="invoicee-search", placeholder="Invoicee")
        content.col1.member_info_tmpl = tf.DIV(id="invoicee-info-tmpl", Class="hidden")
        content.col1.member_info_tmpl.m_id = tf.C("Membership id: ${id}")
        content.col1.member_info_tmpl.br = tf.BR()
        content.col1.member_info_tmpl.address = tf.PRE("${address}")
        content.col1.member_info = tf.DIV(id="invoicee-info", Class="hidden")

        info = tf.TABLE()
        tr = tf.TR()
        cell1 = tf.TD("Start date")
        cell2 = tf.TD()
        cell2.input = tf.INPUT(id="inv-start_date", type="date")
        tr.cells = [cell1, cell2]
        info.tr = tr

        tr = tf.TR()
        cell1 = tf.TD("End date")
        cell2 = tf.TD()
        cell2.input = tf.INPUT(id="inv-end_date", type="date")
        tr.cells = [cell1, cell2]
        info.tr = tr

        tr = tf.TR()
        cell1 = tf.TD("P. O. Number")
        cell2 = tf.TD()
        cell2.input = tf.INPUT(type="text", id="po_number", name="po_number", placeholder="Optional")
        tr.cells = [cell1, cell2]
        info.tr = tr
        content.col2.info = info

        content.notice = tf.DIV(Class="invoice-form-notice")
        content.notice.label = tf.DIV("Optional: Notice/Annoucement (only for this invoice)", Class="note")
        content.notice.text = tf.TEXTAREA(name="notice", id="notice", placeholder="")

        usages = tf.TABLE(id='usages', Class="stripped")
        usages.caption = tf.CAPTION("Usages")
        usages.header = tf.TR()
        usages.header.cells = [tf.TH(name) for name in ('Resource', 'Rate', 'Qty', 'Unit', 'Start-End', 'Total', 'Actions')]

        content.usages = usages

        usage_tmpl = sphc.more.jq_tmpl("usage-tmpl")
        usage_tmpl.tr = tf.TR(id="${id}")
        usage_tmpl.tr.td = tf.TD('${resource_name}')
        usage_tmpl.tr.td = tf.TD('${rate}')
        usage_tmpl.tr.td = tf.TD('${quantity}')
        usage_tmpl.tr.td = tf.TD('${unit}')
        usage_tmpl.tr.td = tf.TD('${start_time} - ${end_time}')
        usage_tmpl.tr.td = tf.TD('${calculated_cost}')
        usage_tmpl.tr.td = tf.TD('')

        content.usage_tmpl = usage_tmpl

        add_usage_form = sphc.more.VForm(id='new-usage-form', action='#')
        add_usage_form.add_field("Resource Name", tf.INPUT(name='resource_name', id='resource_name', nv_attrs=('required',), placeholder="Resource name"))
        add_usage_form.add_field("Rate", tf.INPUT(name='rate', id='rate', nv_attrs=('required',), placeholder="eg. 12.00"), "Do not include currency")
        add_usage_form.add_field("Quantity", tf.INPUT(name='quantity', id='quantity', nv_attrs=('required',), placeholder="eg. 10. Not applicable for time based resource"), fhelp="For non time based resources. Do not include unit")
        add_usage_form.add_field("Unit", tf.INPUT(name='unit', id='unit', nv_attrs=('required',)))
        add_usage_form.add_field("Start", tf.INPUT(name='start_time', id='start_time', nv_attrs=('required',)))
        add_usage_form.add_field("End", tf.INPUT(name='end_time', id='end_time'), "Optional. Only for time based resources.")
        add_usage_form.add_buttons(tf.INPUT(type="button", value="Add", id='submit-usage'))
        add_usage_section = tf.DIV(id='new-usage-section', Class='hidden')
        add_usage_section.form = add_usage_form.build()

        content.add_usage_form = add_usage_section

        invoice_buttons = tf.DIV(Class="invoice-buttons")
        invoice_buttons.status = tf.DIV("Invoice is not saved yet.", id="inv-action-status")
        invoice_buttons.buttons = [ tf.BUTTON("Save", Class="big-button", id="invoice-save"), '→',
            tf.BUTTON("View", Class="big-button", disabled="disabled", id="invoice-view"), '→',
            tf.BUTTON("Send", Class="big-button", disabled="disabled", id="invoice-send")]

        view_invoice_dialog = tf.DIV(id="view_invoice_window", Class='hidden')
        view_invoice_dialog.frame = tf.IFRAME(id="invoice-iframe", src="http://www.google.com", width="500", height="500")
        
        content.new = tf.BUTTON("Add usage", id="new-usage-button")
        content.buttons = invoice_buttons
        content.view_invoice_dialog = view_invoice_dialog 
        content.script = tf.SCRIPT(open("fe/src/js/new_invoice.js").read(), escape=False)

        return container
