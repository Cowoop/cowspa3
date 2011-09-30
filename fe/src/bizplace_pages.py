import sphc
import fe.bases
import commonlib.shared.static as data_lists

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

class BizplaceCreate(BasePage):
    current_nav = 'Places'
    title = 'New Place'
    def content(self):
        container = tf.DIV()

        fields = []

        field = tf.INPUT(type='hidden', id='biz_id', name='biz_id', value=1)
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Name', For="name")
        field.input = tf.INPUT(type='text', id='name', name='name')
        fields.append(field)       
        
        field = tf.DIV()
        field.label = tf.LABEL(content = 'Address', FOR="address")
        field.input = tf.TEXTAREA(id='address', name='address')
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'City', FOR="city")
        field.input = tf.INPUT(type='text', id='city', name='city')
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL('Country', FOR='country')
        field.input = tf.SELECT(id='country', name='country')
        for country in list(data_lists.countries):
            field.input.option = tf.OPTION(country['label'], value=country['name'])
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
        field.label = tf.LABEL('Currency', FOR='currency')
        field.input = tf.SELECT(id='currency', name='currency')
        for currency in data_lists.currencies:
            field.input.option = tf.OPTION(currency['label']+" ("+currency['name']+")", value=currency['name'])
        fields.append(field) 
        
        field = tf.DIV()
        field.button = tf.BUTTON("Save", id='save-btn', type="button")
        fields.append(field)

        form  = tf.FORM(Class='profile-forms', id="createbizplace_form")
        for field in fields:
            form.content = field

        container.form = form
        container.msg = tf.SPAN(id="CreateBizplace-msg")
        container.script = tf.SCRIPT(open("fe/src/js/bizplace_create.js").read(), escape=False, type="text/javascript", language="javascript")
        return container 
