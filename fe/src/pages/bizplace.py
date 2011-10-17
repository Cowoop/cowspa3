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
        container.script = tf.SCRIPT(open("fe/src/js/bizplace_create.js").read(), escape=False, type="text/javascript", language="javascript")
        return container
