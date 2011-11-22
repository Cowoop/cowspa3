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
        cell2.input = tf.INPUT(type='hidden', id="inv-start_date")
        cell2.input = tf.INPUT(id="inv-start_date-vis", Class="inv-dates")
        tr.cells = [cell1, cell2]
        info.tr = tr

        tr = tf.TR()
        cell1 = tf.TD("End date")
        cell2 = tf.TD()
        cell2.input = tf.INPUT(type='hidden', id="inv-end_date")
        cell2.input = tf.INPUT(id="inv-end_date-vis", Class="inv-dates")
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
        usages.header.cells = [tf.TH(name) for name in (tf.INPUT(type="checkbox", Class="all_usages-checkbox"), 'Resource', 'Rate', 'Qty', 'Start-End', 'Total', 'Actions')]

        content.usages = usages

        usage_tmpl = sphc.more.jq_tmpl("usage-tmpl")
        usage_tmpl.tr = tf.TR(id="usage_row-${id}")
        usage_tmpl.tr.td = tf.TD(tf.INPUT(type="checkbox", Class="usage-checkbox"))
        usage_tmpl.tr.td = tf.TD('${resource_name}')
        usage_tmpl.tr.td = tf.TD('${rate}')
        usage_tmpl.tr.td = tf.TD('${quantity}')
        usage_tmpl.tr.td = tf.TD('${start_time} - ${end_time}')
        usage_tmpl.tr.td = tf.TD('${cost}')
        cancel_usage = tf.A('X', title="Remove Usage", href="#", Class="cancel-x cancel-usage", id="cancel_usage-${id}")
        usage_tmpl.tr.td = tf.TD(cancel_usage)

        content.usage_tmpl = usage_tmpl

        #add_usage_form = sphc.more.Form(id='new-usage-form', action='#', classes=['vform'])
        #usage_name = tf.DIV(id="usage_name")
        #usage_name.select = tf.SELECT(id="resource_select", name="resource_select")
        #usage_name.link = tf.A("Custom", id="custom", href="#")
        #add_usage_form.add_field("Resource Name", tf.DIV((usage_name, tf.INPUT(name='resource_name', id='resource_name', placeholder="Resource name", Class="hidden").set_required())))
        #add_usage_form.add_field("Rate", tf.INPUT(name='rate', id='rate', nv_attrs=('required',), placeholder="eg. 12.00"), "Do not include currency")
        #add_usage_form.add_field("Quantity", tf.INPUT(name='quantity', id='quantity', nv_attrs=('required',), placeholder="eg. 10. Not applicable for time based resource"), fhelp="For non time based resources. Do not include unit")
        #add_usage_form.add_field("Start", tf.INPUT(name='start_time', id='start_time', nv_attrs=('required',)))
        #add_usage_form.add_field("End", tf.INPUT(name='end_time', id='end_time'), "Optional. Only for time based resources.")
        #add_usage_form.add_buttons(tf.INPUT(type="button", value="Add", id='submit-usage'))
        #add_usage_section = tf.DIV(id='new-usage-section', Class='hidden')
        #add_usage_section.form = add_usage_form.build()

        #content.add_usage_form = add_usage_section

        invoice_buttons = tf.DIV(Class="invoice-buttons")
        invoice_buttons.status = tf.DIV("Invoice is not saved yet.", id="inv-action-status")
        invoice_buttons.buttons = [ tf.BUTTON("Save", Class="big-button", id="invoice-save"), '→',
            tf.BUTTON("View", Class="big-button", disabled="disabled", id="invoice-view"), '→',
            tf.BUTTON("Send", Class="big-button", disabled="disabled", id="invoice-send")]

        view_invoice_dialog = tf.DIV(id="view_invoice_window", Class='hidden')
        view_invoice_dialog.frame = tf.IFRAME(id="invoice-iframe", src="#", width="800", height="600")
        
        resource_select_tmpl = sphc.more.jq_tmpl("resource-tmpl")
        resource_select_tmpl.option = tf.OPTION("${name}", id="resource_${id}", value="${name}")
        
        #content.new = tf.BUTTON("Add usage", id="new-usage-button")
        content.buttons = invoice_buttons
        content.resource_select_tmpl = resource_select_tmpl
        content.view_invoice_dialog = view_invoice_dialog 
        content.script = tf.SCRIPT(open("fe/src/js/new_invoice.js").read(), escape=False)

        return container
        
class Preferences(BasePage):

    title = "Invoice Preferences"
    current_nav = 'Invoicing'
    
    def content(self):
        container = tf.DIV()
        
        edit = tf.DIV(Class="edit-link-box")
        edit.link = tf.A("Edit", id='edit-link', href='#edit')
        container.edit = edit
        
        view_section = tf.DIV(id='view-section')
        view_section.logo = tf.DIV(Class="field-container")
        view_section.logo.label = tf.DIV("Logo", Class="field-name")
        view_section.logo.value = tf.IMG(Class="invoice-logo", id="data-logo", alt="Logo is not available")
        view_section.email_text = tf.DIV(Class="field-container")
        view_section.email_text.label = tf.DIV("Email Text", Class="field-name")
        view_section.email_text.value = tf.DIV(id="data-email_text", Class="field-value")
        view_section.terms = tf.DIV(Class="field-container")
        view_section.terms.label = tf.DIV("Terms And Conditions", Class="field-name")
        view_section.terms.value = tf.DIV(id="data-terms_and_conditions", Class="field-value")
        view_section.due_date = tf.DIV(Class="field-container")
        view_section.due_date.label = tf.DIV("Invoice Due Date", Class="field-name")
        view_section.due_date.value = tf.DIV(id="data-due_date", Class="field-value")
        view_section.bcc = tf.DIV(Class="field-container")
        view_section.bcc.label = tf.DIV("Bcc Invoice", Class="field-name")
        view_section.bcc.value = tf.DIV(id="data-bcc_email", Class="field-value")
        view_section.bank_details = tf.DIV(Class="field-container")
        view_section.bank_details.label = tf.DIV("Bank Details", Class="field-name")
        view_section.bank_details.value = tf.DIV(id="data-bank_details", Class="field-value")
        container.view_form = view_section
        
        edit_form = sphc.more.Form(id='preferences_edit_form', classes=['hform'], enctype='multipart/form-data')
        edit_form.add_field("Logo", tf.INPUT(name="logo", id="logo", type="file", accept="image/*"), "Suggested Image Dimensions : 150x150.")
        edit_form.add_field("Email Text", tf.TEXTAREA(Class="changed-data", name="email_text", id="email_text"))
        edit_form.add_field("Terms And Conditions", tf.TEXTAREA(Class="changed-data", name="terms_and_conditions", id="terms_and_conditions"))
        edit_form.add_field("Invoice Due Date",tf.INPUT(Class="changed-data", name="due_date", id="due_date", type="number"), "Days after sending invoice")
        edit_form.add_field("Bcc Invoice", tf.INPUT(Class="changed-data", name="bcc_email", id="bcc_email", type="email"), "Invoices will be Bcced to this Email id")
        edit_form.add_field("Bank Details", tf.TEXTAREA(Class="changed-data", name="bank_details", id="bank_details"))
        edit_form.add_buttons(tf.INPUT(type="button", value="Save", id='save-btn'), tf.INPUT(type="button", value="Cancel", id='cancel-btn'))
        edit_section = tf.DIV(id='edit-section', Class='hidden')
        edit_section.form = edit_form.build()
        edit_section.msg = tf.SPAN(id="edit_invoicepref-msg")
        container.edit_form = edit_section
        
        container.script = tf.SCRIPT(open("fe/src/js/invoice_preferences.js").read(), escape=False)
        
        return container
        
class History(BasePage):

    title = "Invoice History"
    current_nav = 'Invoicing'
    
    def content(self):
        container = tf.DIV()
        container.table = tf.TABLE(id="history_table")
        container.view_invoice_dialog = tf.DIV(id="view_invoice_window", Class='hidden')
        container.view_invoice_dialog.frame = tf.IFRAME(id="invoice-iframe", src="#", width="800", height="600")
        container.script = tf.SCRIPT(open("fe/src/js/invoice_history.js").read(), escape=False)
        return container
