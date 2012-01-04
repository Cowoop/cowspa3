import sphc
import fe.bases

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

class Taxes(BasePage):
    current_nav = 'Taxes'
    title = 'Taxes'

    def content(self):
        container = tf.DIV()
        taxes = sphc.more.Form(id="taxation", Class="hform")
        taxes.add_field("Prices include Taxes", tf.INPUT(id="taxes_included", type="checkbox"), \
            "If unchecked tax amount will be added to final usage prices")
        add_tax = tf.DIV(id="add_tax")
        add_tax.name = tf.DIV(tf.INPUT(placeholder="Tax name", type="text", id='new_tax'), Class='tax-name')
        add_tax.value = tf.DIV([tf.INPUT(placeholder="Value: eg. 10 for 10%", type="number", id='new_value', step="0.1"), tf.span("%")], Class='tax-value')
        add_tax.action = tf.DIV(tf.BUTTON("Add", type="button", id="add_tax-btn"), Class="tax-delete")
        taxes.add_field("Taxes", tf.DIV(add_tax, id="taxes_list"))
        taxes.add_buttons(tf.BUTTON("Save", id="save-btn", type="submit"))
        tax_template = sphc.more.jq_tmpl('tax_tmpl')
        tax_template.new_tax = tf.DIV(Class="new-tax")
        tax_template.new_tax.name = tf.DIV(tf.INPUT(type="text", value="${name}", Class="new-name").set_required(), Class='tax-name')
        tax_template.new_tax.value = tf.DIV([tf.INPUT(type="number", value="${value}", Class="new-value", step="0.1").set_required(), tf.span("%")], Class='tax-value')
        tax_template.new_tax.delete = tf.DIV(tf.A("X", href="#"), Class="tax-delete remove-tax")

        container.taxes = taxes.build()
        container.template = tax_template
        container.script = sphc.more.script_fromfile("fe/src/js/taxes.js")
        return container
