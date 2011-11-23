import sphc
import fe.bases

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

def get_tariff_form():
    form  = sphc.more.Form(classes=['hform'], id="tariff_form", style="display:none")
    form.add_field('Name', tf.INPUT(type='text', id='name', name='name'))
    form.add_field('Description', tf.TEXTAREA(id='short_description', name='short_description'))
    form.add_field('Default price', tf.INPUT(id='default_price', name='default_price'))
    form.msg = tf.SPAN(id="tariff-msg")

    return form

class PlanCreate(BasePage):
    current_tab = 'new'
    title = 'Tariffs'
    def content(self):
        container = tf.DIV()

        new_tariff = tf.BUTTON("New Tariff", id="new-tariff", type='button')
        container.button = new_tariff

        tariffs = tf.DIV(id="tariff_list")
        tariff_tmpl = sphc.more.jq_tmpl('tariff_tmpl')
        tariff_tmpl.box = tf.DIV(Class='tariff-box')
        tariff_tmpl.box.link = tf.A("${name}", id='edit-link_${id}', href='#/${id}/edit', Class='tariff-title')
        tariff_tmpl.box.short_description = tf.DIV("${short_description}", Class='tariff-description')

        tariffs.tariff_tmpl = tariff_tmpl
        tariffs.left = tf.DIV(id="left")
        tariffs.right = tf.DIV(id="right")

        container.tariffs = tariffs

        #                                   New PLAN
        form = get_tariff_form()
        form.add_buttons(tf.BUTTON("Create", id='save-btn', type="submit"), tf.BUTTON("Cancel", id='cancel-btn', type='button'))

        container.form = form.build()
        container.script = sphc.more.script_fromfile("fe/src/js/plan_create.js")
        return container
