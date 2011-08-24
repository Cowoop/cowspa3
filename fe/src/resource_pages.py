import sphc
import fe.bases
import commonlib.shared.static_data as types

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

class ResourceCreate(BasePage):
    current_tab = 'create'
    title = 'New Resource'
    def  main(self):
        container = tf.DIV()

        fields = []

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Name : ', For='name')
        field.input = tf.INPUT(type='text', id='name', name='name')
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL('Type : ', FOR='type')
        field.input = tf.SELECT(id='type', name='type')
        for type in types.resource_types:
            field.input.option = tf.OPTION(type, value = type)
            
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Short Description : ', FOR="short_description")
        field.input = tf.TEXTAREA( id='short_description', name='short_description', rows=2, cols=25)
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Long Description : ', FOR="long_description")
        field.input = tf.TEXTAREA(id='long_description', name='long_description', rows=5, cols=25)
        fields.append(field)


        field = tf.DIV()
        field.label = tf.LABEL(content = 'Quantity Unit : ', FOR='quantity_unit')
        field.input = tf.INPUT(type='text', id='quantity_unit', name='quantity_unit')
        fields.append(field)

        field = tf.DIV()
        field.input = tf.INPUT(type='checkbox', id='time_based', name='time_based')
        field.text = 'Time Based'
        fields.append(field)
        
        field = tf.DIV()
        field.button = tf.BUTTON("Save", id='save-btn', type='button')
        fields.append(field)

        form  = tf.FORM(id="createresource_form")
        for field in fields:
            field.line = tf.BR()
            form.content = field
    
        container.form = form
        container.msg = tf.SPAN(id="CreateResource-msg")
        container.script = tf.SCRIPT(open("fe/src/js/resource_create.js").read(), escape=False, type="text/javascript", language="javascript")
        return container
