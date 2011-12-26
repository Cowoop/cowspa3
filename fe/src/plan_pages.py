import sphc
import fe.bases

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

def get_tariff_form(create_form=True):
    form  = sphc.more.Form(classes=['hform'], id="tariff_form", style="display:none")
    about = form.add(sphc.more.Fieldset())
    about.add(sphc.tf.LEGEND('Details'))
    about.add_field('Name', tf.INPUT(type='text', id='name',
        name='name').set_required())
    about.add_field('Description', tf.TEXTAREA(id='short_description', name='short_description'))
    if create_form: about.add_field('Default Price', tf.INPUT(id='default_price', name='default_price').set_required())

    return form

class CreateTariff(BasePage):
    title = 'New Tariff'
    current_nav = 'Admin'
    def content(self):
        container = tf.DIV()

        form = get_tariff_form()
        form.add_buttons(tf.BUTTON("Create", id='save-btn', type="submit"), tf.BUTTON("Cancel", id='cancel-btn', type='button'))

        container.form = form.build()
        container.script = sphc.more.script_fromfile("fe/src/js/plan_create.js")
        return container

class ListTariff(BasePage):
    title = 'Tariffs'
    current_nav = 'Admin'
    content_menu = [tf.A('Create New +', href="/${lang}/${theme}/tariff/new", Class="item big-button")]
    def content(self):
        container = tf.DIV()

        tariffs = tf.DIV(id="tariff_list")
        tariff_tmpl = sphc.more.jq_tmpl('tariff_tmpl')
        tariff_tmpl.box = tf.DIV(Class='tariff-box')
        tariff_tmpl.box.link = tf.A("${name}", id='edit-link_${id}', href='#/${id}/edit', Class='tariff-title')
        tariff_tmpl.box.short_description = tf.DIV("${short_description}", Class='tariff-description')

        tariffs.tariff_tmpl = tariff_tmpl
        tariffs.left = tf.DIV(id="left")
        tariffs.right = tf.DIV(id="right")

        pricing_content = tf.DIV(id="tariff-pricing-content", Class="hidden")
        pricing =  sphc.more.Fieldset()
        pricing.add(sphc.tf.LEGEND('Pricing'))

        pricing_tmpl = sphc.more.jq_tmpl("old-pricing-tmpl")
        pricing_tmpl.pricing = tf.DIV(Class="pricing")

        view_pricing = tf.DIV(id="pricing-${id}")
        view_pricing.starts = tf.SPAN("${starts}", Class="pricing-date", id="pricing_date-${id}")
        view_pricing.amount = tf.SPAN("${amount}", Class="pricing-amt", id="pricing_amount-${id}")
        view_pricing.edit = tf.SPAN(tf.A("Edit", id="pedit-${id}", Class="pricing_edit-link"))
        view_pricing.cancel = tf.SPAN(tf.A("X", id="pricing_${id}", Class="cancel-x"))
        edit_pricing = tf.FORM(id="edit_pricing-${id}", Class="edit-pricing hidden", method="POST")
        edit_pricing.start_vis = tf.SPAN(tf.INPUT(placeholder="From date", type="text", id='edit_starts_vis-${id}').set_required())
        edit_pricing.starts = tf.INPUT(id='edit_starts-${id}', type="hidden", value="-")
        edit_pricing.amount = tf.SPAN(tf.INPUT(type="text", id='edit_amount-${id}', value="${amount}").set_required())
        edit_pricing.save = tf.SPAN(tf.BUTTON("Save", id="save_edit-${id}", type="submit"))
        edit_pricing.cancel = tf.SPAN(tf.BUTTON("Cancel", type="button", Class="edit-cancel", id="cancel_edit-${id}"))
        pricing_tmpl.pricing.view = view_pricing
        pricing_tmpl.pricing.edit = edit_pricing

        pricing.add(pricing_tmpl)

        new = tf.FORM(id="new-pricing", method="POST") #, Class="hidden")
        new.starts_vis = tf.SPAN(tf.INPUT(placeholder="From date", type="text", id='new-starts-vis'))
        new.starts = tf.INPUT(id='new-starts', type="hidden").set_required()
        new.amount = tf.SPAN(tf.INPUT(placeholder="New price", type="text", id='new-amount').set_required())
        new.action = tf.SPAN(tf.BUTTON("Save", type="submit"))
        pricing.add(new)

        table = tf.DIV(id="old-pricings", Class="grid")
        pricing.add(table)

        pricing_content.fldset = pricing.build()

        container.tariffs = tariffs

        form = get_tariff_form(create_form=False)
        form.add_buttons(tf.BUTTON("Save", id='save-btn', type="submit"), tf.BUTTON("Cancel", id='cancel-btn', type='button'))

        container.profile_form = form.build()

        container.pricing = pricing_content
        #container.pricing.pricing_contents = pricing

        container.script = sphc.more.script_fromfile("fe/src/js/list_tariffs.js")
        return container
