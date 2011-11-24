import sphc
import fe.bases

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

def get_tariff_form():
    form  = sphc.more.Form(classes=['hform'], id="tariff_form", style="display:none")
    form.add_field('Name', tf.INPUT(type='text', id='name',
        name='name').set_required())
    form.add_field('Description', tf.TEXTAREA(id='short_description', name='short_description'))
#    defprice = tf.DIV(id='def_price') #Need to hide when editing hence separate DIV
#    defprice.label = tf.LABEL('Default Price')
#    defprice.fld =  tf.INPUT(id='default_price', name='default_price').set_required()
#    form.add(defprice)

    return form

class CreateTariff(BasePage):
    #current_tab = 'new'
    title = 'New Tariff'
    def content(self):
        container = tf.DIV()

        form = get_tariff_form()
        form.add_field('Default Price', tf.INPUT(id='default_price', name='default_price').set_required())
        form.add_buttons(tf.BUTTON("Create", id='save-btn', type="submit"), tf.BUTTON("Cancel", id='cancel-btn', type='button'))

        container.form = form.build()
        container.script = sphc.more.script_fromfile("fe/src/js/plan_create.js")
        return container

class ListTariff(BasePage):
    #current_tab = 'new'
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

        form = get_tariff_form()
        form.add_buttons(tf.BUTTON("Save", id='save-btn', type="submit"), tf.BUTTON("Cancel", id='cancel-btn', type='button'))

        container.form = form.build()
        container.script = sphc.more.script_fromfile("fe/src/js/list_tariffs.js")
        return container
