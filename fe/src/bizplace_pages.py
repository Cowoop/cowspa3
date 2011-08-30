import sphc
import fe.bases
import pycountry

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

class BizplaceCreate(BasePage):
    current_nav = 'Places'
    title = 'New Place'
    def content(self):
        container = tf.DIV()

        fields = []

        field = tf.INPUT(type='hidden', id='biz', name='biz', value=1)
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Name', For="name")
        field.input = tf.INPUT(type='text', id='name', name='name')
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Address', FOR="address")
        field.input = tf.INPUT(type='text', id='address', name='address')
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'City', FOR="city")
        field.input = tf.INPUT(type='text', id='city', name='city')
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL('Country', FOR='country')
        field.input = tf.SELECT(id='country', name='country')
        for country in list(pycountry.countries):
            field.input.option = tf.OPTION(country.name.encode("utf-8"), value=country.name.encode("utf-8"))
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Email', FOR='email')
        field.input = tf.INPUT(type='email', id='email', name='email')
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Short Description', FOR="short_desciption")
        field.input = tf.TEXTAREA( id='short_description', name='short_description', rows=2, cols=25)
        fields.append(field)

        field = tf.DIV()
        field.button = tf.BUTTON("Save", id='save-btn')
        fields.append(field)

        form  = tf.FORM(id="createbizplace_form")
        for field in fields:
            form.content = field

        container.form = form
        container.msg = tf.SPAN(id="CreateBizplace-msg")
        container.script = tf.SCRIPT(open("fe/src/js/bizplace_create.js").read(), escape=False, type="text/javascript", language="javascript")
        return container 
