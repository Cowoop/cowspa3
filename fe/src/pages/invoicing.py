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
        usages.header.cells = [tf.TH(name) for name in (tf.INPUT(type="checkbox", Class="all_usages-checkbox", checked="on"), 'Resource', 'Qty', 'Start-End', 'Total')]

        content.usages = usages

        usage_tmpl = sphc.more.jq_tmpl("usage-tmpl")
        usage_tmpl.tr = tf.TR(id="usage_row-${id}")
        usage_tmpl.tr.td = tf.TD(tf.INPUT(type="checkbox", Class="usage-checkbox", checked="on"))
        usage_tmpl.tr.td = tf.TD('${resource_name}')
        usage_tmpl.tr.td = tf.TD('${quantity}')
        usage_tmpl.tr.td = tf.TD('${start_time} - ${end_time}')
        usage_tmpl.tr.td = tf.TD('${cost}')
        #cancel_usage = tf.A('X', title="Remove Usage", href="#", Class="cancel-x cancel-usage", id="cancel_usage-${id}")
        #usage_tmpl.tr.td = tf.TD(cancel_usage)

        content.usage_tmpl = usage_tmpl

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
        main = tf.DIV(id="invoicepref-main")

        view_section = tf.DIV(id='view-section', Class='floatfix')
        view_section.edit = tf.DIV(Class="edit-link-box")
        view_section.edit.link = tf.A("Edit", id='edit-link', href='#main')

        view_section.logo = tf.DIV(Class="field-container")
        view_section.logo.label = tf.DIV("Logo", Class="field-name")
        view_section.logo.value = tf.IMG(Class="invoice-logo", id="data-logo", alt="Logo is not available", title="Image Not Found")
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
        view_section.free_text1 = tf.DIV(Class="field-container")
        view_section.free_text1.label = tf.DIV("Free Text1", Class="field-name")
        view_section.free_text1.value = tf.DIV(id="data-freetext1", Class="field-value")
        view_section.free_text2 = tf.DIV(Class="field-container")
        view_section.free_text2.label = tf.DIV("Free Text2", Class="field-name")
        view_section.free_text2.value = tf.DIV(id="data-freetext2", Class="field-value")
        main.view = view_section

        edit_form = sphc.more.Form(id='preferences_edit_form', classes=['hform'], enctype='multipart/form-data')
        edit_form.add_field("Logo", tf.INPUT(name="logo", id="logo", type="file", accept="image/*"), "Suggested Image Dimensions : 150x150.")
        edit_form.add_field("Terms And Conditions", tf.TEXTAREA(Class="changed-data", name="terms_and_conditions", id="terms_and_conditions"))
        edit_form.add_field("Invoice Due Date",tf.INPUT(Class="changed-data", name="due_date", id="due_date", type="number"), "Days after sending invoice")
        edit_form.add_field("Bcc Invoice", tf.INPUT(Class="changed-data", name="bcc_email", id="bcc_email", type="email"), "Invoices will be Bcced to this Email id")
        edit_form.add_field("Bank Details", tf.TEXTAREA(Class="changed-data", name="bank_details", id="bank_details"))
        edit_form.add_field("Invoice Free Text (Page 1)", tf.TEXTAREA(Class="changed-data", name="freetext1", id="freetext1"), 'Text will appear before "Usage summary" section')
        edit_form.add_field("Invoice Free Text (Last Page)", tf.TEXTAREA(Class="changed-data", name="freetext2", id="freetext2"), 'Text will appear after "Usage details" section')
        edit_form.add_buttons(tf.INPUT(type="button", value="Save", id='save-btn'), tf.INPUT(type="button", value="Cancel", id='cancel-btn'))
        edit_section = tf.DIV(id='edit-section', Class='hidden')
        edit_section.form = edit_form.build()
        edit_section.msg = tf.SPAN(id="edit_invoicepref-msg")
        main.edit_form = edit_section

        email = tf.DIV(id="invoicepref-email")

        view_section2 = tf.DIV(Class="floatfix", id='view-section2')
        view_section2.edit = tf.DIV(Class="edit-link-box")
        view_section2.edit.link = tf.A("Edit", id='edit-link2', href='#email')

        view_section2.email_text = tf.DIV(Class="field-container")
        view_section2.email_text.label = tf.DIV("Email Text", Class="field-name")
        view_section2.email_text.value = tf.DIV(id="data-email_text", Class="field-value")
        email.view_form2 = view_section2

        tax_edit_template = sphc.more.jq_tmpl(id="tax_edit_template")
        tax_edit_template.field = tf.DIV(Class="field", id="tax-${id}")
        tax_edit_template.field.name = tf.DIV(tf.INPUT(id="tax_name-${id}" , type="text"), Class="tax-name")
        tax_edit_template.field.value = tf.DIV(tf.INPUT(id="tax_value-${id}", type="text"), Class="tax-value")
        tax_edit_template.field.value = tf.DIV(tf.A("X", id="tax_delete-${id}", href="#"), Class="tax-delete")
        main.tax_edit_template = tax_edit_template

        edit_form2 = sphc.more.Form(id='preferences_edit_form2', classes=['hform'])
        edit_form2.add_field("Email Text", tf.TEXTAREA(name="email_text", id="invoice-email_text"))
        edit_form2.add_buttons(tf.INPUT(type="button", value="Save", id='save-btn2'), tf.INPUT(type="button", value="Cancel", id='cancel-btn2'))
        edit_section2 = tf.DIV(id='edit-section2', Class="hidden")
        edit_section2.form = edit_form2.build()
        email.edit_form = edit_section2
         # Tabs
        container.tabs = tf.DIV(id="invoicepref_tabs")
        container.tabs.list = tf.UL()
        container.tabs.list.tab1 = tf.li(tf.A("Main", href="#invoicepref-main"))
        container.tabs.list.tab2 = tf.li(tf.A("Email", href="#invoicepref-email"))
        container.tabs.main = main
        container.tabs.email = email

        container.script = tf.SCRIPT(open("fe/src/js/invoice_preferences.js").read(), escape=False)
        container.clear = sphc.more.clear()

        return container

class History(BasePage):

    title = "Invoice History"
    current_nav = 'Invoicing'

    def content(self):
        container = tf.DIV()
        container.invoice_row = sphc.more.jq_tmpl('invoice_row-tmpl')
        container.invoice_row.tmpl = tf.TR()
        container.invoice_row.tmpl.number = tf.TD('${number || "-"}')
        container.invoice_row.tmpl.name = tf.TD('${member_name}')
        container.invoice_row.tmpl.total = tf.TD('${total}')
        container.invoice_row.tmpl.sent = tf.TD('${isodate2fdate(sent) || "-"}')
        container.invoice_row.tmpl.cond = '{{if (sent)}}'
        container.invoice_row.tmpl.actions = tf.TD([tf.A('View ', id='view-${id}', Class='view-invoice'), ' | ', \
            tf.A('Resend', id='send-${id}', Class='send-invoice')])
        container.invoice_row.tmpl.cond_end = '{{/if}}'
        container.invoice_row.tmpl.cond = '{{if (!sent)}}'
        container.invoice_row.tmpl.actions = tf.TD([tf.A('View', id='view-${id}', Class='view-invoice'), ' | ', \
            tf.A('Send', id='send-${id}', Class='send-invoice'), ' | ', \
            tf.A('X', id='delete-${id}', Class='cancel-x delete-invoice')])
        container.invoice_row.tmpl.cond_end = '{{/if}}'
        container.table = tf.TABLE(id="history_table")
        container.table.head = tf.THEAD()
        container.table.head.cols = tf.TR([tf.TH(name) for name in ('Number', 'Member', 'Amount', 'Sent', 'Actions')])
        container.view_invoice_dialog = tf.DIV(id="view_invoice_window", Class='hidden')
        container.view_invoice_dialog.frame = tf.IFRAME(id="invoice-iframe", src="#", width="800", height="600")
        send_invoice = sphc.more.Form(id='send_invoice-form', classes=['vform', 'hidden'])
        send_invoice.add_field("Email Text", tf.TEXTAREA(id="email_text"))
        send_invoice.add_buttons(tf.INPUT(id="send-btn", type="button", value="Send"), tf.INPUT(id="send_cancel-btn", type="button", value="Cancel"))
        container.send_invoice = send_invoice.build()
        container.script = sphc.more.script_fromfile("fe/src/js/invoice_history.js")
        return container

class Uninvoiced(BasePage):

    title = "Uninvoiced usages"
    current_nav = "Invoicing"

    def content(self):
        container = tf.DIV()
        container.view_invoice_dialog = tf.DIV(id="view_invoice_window", Class='hidden')
        container.view_invoice_dialog.frame = tf.IFRAME(id="invoice-iframe", src="#", width="800", height="600")

        container.dashboard = tf.DIV(id='invoicing-dashboard')
        form = sphc.more.Form(id='uninvoiced-form', action='#', classes=['hform'])
        form.add_field('Usage types to include', tf.SPAN([tf.INPUT(name='only_tariff', type='radio', value='on'), 'Only tariffs', tf.INPUT(name='only_tariff', type='radio', checked='checked', value='off'), 'All usages (including tariffs)']))
        form.add_field('Zero usage cost members', tf.INPUT(name='zero_usage_members', type='checkbox', checked='on'), 'Generate invoices even if total usages cost is zero')
        form.add_field('Usages start on or before', tf.INPUT(id='uninvoiced-start-vis', type='text'))
        form.add(tf.INPUT(name='start', id='uninvoiced-start', type='hidden'))
        form.add_buttons(tf.INPUT(id="send-btn", type="submit", value="Generate Invoices"))
        container.dashboard.form = form.build()

        config_form = sphc.more.Form(Class='vform', id='invoice-config-form_${member.id}')
        config_form.add_field("P.O. Number", tf.INPUT(type='text', id='invoice-ponumber_${member.id}', Class='invoice-ponumber'), "Optional: Purchase order number")
        config_form.add_field("Email text", tf.TEXTAREA('${invoice_email_text_default}', id='invoice-email-text_${member.id}', Class='invoice-email-text email-text'), "Optional: Customize invoice email text")
        config_form.add_buttons(tf.INPUT(value="Save", type="submit", id="save-inv-config_${member.id}", Class='save-inv-config'))
        container.actions = tf.DIV(Class='invoicing-actions hidden')
        container.actions.buttons = tf.DIV([tf.BUTTON("Send selected", id="send-invoices"), tf.BUTTON("Delete selected", id="delete-invoices")], Class="button-bar")
        container.actions.bills = tf.TABLE(id='bills-section', Class='stripped')
        container.actions.bills.header = tf.TR([tf.TH(tf.INPUT(type='checkbox', id='invoice-select-all')), \
            tf.TH("Name"), tf.TH("Amount"), tf.TH()])
        container.actions.bill_template = sphc.more.jq_tmpl(id='bill-template')
        container.actions.bill_template.bill = tf.TR(id='bill-${member.id}')
        container.actions.bill_template.bill.select = tf.TD(tf.INPUT(type='checkbox', id='select-${member.id}', Class='invoice-select'))
        container.actions.bill_template.bill.name = tf.TD('${member.name}')
        container.actions.bill_template.bill.summary = tf.TD('${total}')
        container.actions.bill_template.bill.status = tf.TD(id='bill-status-${member.id}')
        container.actions.bill_template.bill.status.msg = tf.C('Generating Invoice ..', id='gen-invoice-msg_${member.id}')
        container.actions.bill_template.bill.status.actions = tf.DIV([tf.A('View', id='view-invoice_${member.id}'), ' | ',  tf.A('Email', id='email-invoice_${member.id}')], id='invoice-actions_${member.id}', Class='hidden')
        container.actions.bill_template.bill.status.config = tf.DIV(config_form.build(), id='invoice-config_${member.id}', Class='hidden')
        container.script = sphc.more.script_fromfile("fe/src/js/uninvoiced.js")
        return container
