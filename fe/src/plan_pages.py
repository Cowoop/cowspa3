import sphc
import fe.bases

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

class PlanCreate(BasePage):
    current_tab = 'create'
    title = 'New Plan'
    def content(self):
        container = tf.DIV()

        fields = []

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Name : ', For='plan_name')
        field.input = tf.INPUT(type='text', id='name', name='name')
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Description : ', FOR="description")
        field.input = tf.TEXTAREA(id='description', name='description', rows=2, cols=25)
        fields.append(field)
        
        field = tf.DIV()
        field.button = tf.BUTTON("Save", id='save-btn', type='button')
        fields.append(field)

        form  = tf.FORM(id="createplan_form")
        for field in fields:
            field.line = tf.BR()
            form.content = field
    
        container.form = form
        container.msg = tf.SPAN(id="CreatePlan-msg")
        container.script = tf.SCRIPT(open("fe/src/js/plan_create.js").read(), escape=False, type="text/javascript", language="javascript")
        return container
