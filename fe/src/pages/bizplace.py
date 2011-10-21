import sphc
import fe.bases
import commonlib.shared.static as data_lists

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

class Create(BasePage):
    current_nav = 'Locations'
    title = 'New Location'
    def content(self):
        container = tf.DIV()

        form = sphc.more.Form(id='createbizplace_form', classes=['hform'], enctype='multipart/form-data')

        form.add_field(input=tf.INPUT(type='hidden', id='biz_id', name='biz_id', value=1), custom=True)
        form.add_field('Name', tf.INPUT(type='text', id='name', name='name').set_required())
        form.add_field('Address', tf.TEXTAREA(id='address', name='address'))
        form.add_field('City', tf.INPUT(type='text', id='city', name='city'))
        field = tf.SELECT(id='country', name='country')
        for country in list(data_lists.countries):
            field.option = tf.OPTION(country['label'], value=country['name'])
        form.add_field('Country', field)
        form.add_field('Email', tf.INPUT(type='email', id='email', name='email').set_required())
        form.add_field('Short Description', tf.TEXTAREA( id='short_description', name='short_description', rows=2, cols=25))
        field = tf.SELECT(id='currency', name='currency')
        for currency in data_lists.currencies:
            field.option = tf.OPTION(currency['label']+" ("+currency['name']+")", value=currency['name'])
        form.add_field('Currency', field)
        form.add_buttons(tf.BUTTON("Create", id='save-btn', type="submit"))

        container.form = form.build()
        container.script = sphc.more.script_fromfile("fe/src/js/bizplace_create.js")
        return container

class List(BasePage):

    title = "List Locations"
    current_nav = 'Locations'

    def content(self):
        container = tf.DIV()

        content = tf.DIV(id='location-list')
        container.content = content

        location_tmpl = sphc.more.jq_tmpl('loc_tmpl')
        location_tmpl.box = tf.DIV(Class='location-box')
        location_tmpl.box.link = tf.A("${name}", id='edit-link_${id}', href='#edit', Class='location-title')
        location_tmpl.box.city = tf.LABEL("   ${city}, ${country}", Class='location-info')
        location_tmpl.box.short_description = tf.DIV("${short_description}", Class='location-info')
        container.loctmpl = location_tmpl

        container.script = sphc.more.script_fromfile("fe/src/js/list_locations.js")

        return container

