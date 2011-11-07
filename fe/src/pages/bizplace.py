import sphc
import fe.bases
import commonlib.shared.static as data_lists

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

def get_location_form():
    form = sphc.more.Form(id='bizplace_form', classes=['hform'], enctype='multipart/form-data')

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
    
    return form

class Create(BasePage):
    current_nav = 'Locations'
    title = 'New Location'

    def content(self):
        container = tf.DIV()
        form = get_location_form()
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
        location_tmpl.box.link = tf.A("${name}", id='edit-link_${id}', href='#/${id}/', Class='location-title')
        location_tmpl.box.city = tf.LABEL("${city}, ${country}", Class='location-info')
        location_tmpl.box.short_description = tf.DIV("${short_description}", Class='location-description')
        container.loctmpl = location_tmpl

        # View Location Details       
        edit = tf.DIV(Class="edit-link-box")
        edit.link = tf.A("Edit", id='edit-link', href='')
        fields = [edit]

        cancel = tf.DIV(Class="edit-link-box")
        cancel.link = tf.A("Back to List", id='cancel-link', href='')
        fields.append(cancel)

        field_data = [('Name', 'name'),
            ('Address', 'address'),
            ('City', 'city'),
            ('Country', 'country'),
            ('Email', 'email'),
            ('Short description', 'short_description'),
            ('Currency', 'currency')
            ]
        for label, name in field_data:
            field = tf.DIV(Class="field-container")
            field.label = tf.DIV(label, Class="field-name")
            field.value = tf.DIV(id=name, Class="field-value")
            fields.append(field)

        view = tf.DIV(Class='location-forms', id="location_view_form", style="display:none")
        view.fields= fields

        # # This should appear near Edit Button
        # view.button = tf.BUTTON("Cancel", id='cancel-btn', type="button")

        container.view = view

        form = get_location_form()
        buttons = tf.DIV(Class="buttons")
        buttons.button = tf.BUTTON("Save", id='save-btn', type='submit')
        buttons.button = tf.BUTTON("Cancel", id='cancel-btn', type='button')
        form.add_buttons(buttons)

        container.form = form.build()
        container.script = sphc.more.script_fromfile("fe/src/js/list_locations.js")

        return container

