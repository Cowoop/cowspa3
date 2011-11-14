import sphc
import fe.bases

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

class PlanCreate(BasePage):
    current_tab = 'new'
    title = 'Tariffs'
    def content(self):
        container = tf.DIV()

        new_tariff = tf.BUTTON("New Tariff", id="new-tariff", type='button')
        container.button = new_tariff

        tariffs = tf.DIV(id="tariff_list")
        tariffs.left = tf.DIV(id="left")
        tariffs.right = tf.DIV(id="right")

        container.tariffs = tariffs

        #                                   New PLAN
        fields = []

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Name : ', For='tariff_name')
        field.input = tf.INPUT(type='text', id='name', name='name')
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Description : ', FOR="short_description")
        field.input = tf.TEXTAREA(id='short_description', name='short_description', rows=2, cols=25)
        fields.append(field)

        field = tf.DIV()
        field.save = tf.BUTTON("Save", id='save-btn', type='button')
        field.cancel = tf.BUTTON("Cancel", id='cancel-btn', type='button')
        fields.append(field)

        form  = tf.FORM(Class='profile-forms', id="createtariff_form", style="display:none")
        for field in fields:
            field.line = tf.BR()
            form.content = field
        form.msg = tf.SPAN(id="CreatePlan-msg")
        
        container.form = form
        container.script = tf.SCRIPT(open("fe/src/js/plan_create.js").read(), escape=False, type="text/javascript", language="javascript")
        return container
