import sphc
import fe.bases

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

class LoginPage(fe.bases.CSAnonPage):
    title = "Cowspa | Login"
    def main(self):
        container = tf.DIV()
        username = tf.INPUT(**{ 'type':"TEXT", 'id':'username', 'name':"username", 'placeholder':"Username", 'data-bind':'value: username' })
        password = tf.INPUT(**{ 'type':"PASSWORD", 'id':'password', 'name':"password", 'placeholder':"Password", 'data-bind':'value: password'})
        submit = tf.BUTTON("Log In", **{'id':'login-btn', 'data-bind':'click: clicked'})
        form = tf.FORM(id = "login_form")
        form.fields = [username, password, submit]
        container.form = form
        container.msg = tf.SPAN(id="login-msg")
        container.script = tf.SCRIPT(open("fe/src/js/login.js").read(), escape=False, type="text/javascript", language="javascript")
        return container

class InvoicingPage(BasePage):
    current_tab = 'invoicing'
    title = 'Invoicing'

    def  main(self):
        return tf.H1("Invoicing")

class SuperuserCreate(BasePage):
    current_tab = 'create'
    title = 'New Super User'
    def  main(self):
        container = tf.DIV()
        
        fields = []

        field = tf.DIV()
        field.label = tf.LABEL(content = 'First Name : ', For="first_name")
        field.input = tf.INPUT(**{'type':'text', 'id':'first_name', 'name':'first_name', 'data-bind':'value: first_name'})
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL('Bizplace ID : ', FOR='bizplace_id')
        field.input = tf.SELECT(**{'id':'bizplace_ids', 'name':'bizplace_ids', 'data-bind':'selectedOptions: bizplace_id'})
        field.input.option = tf.OPTION("1", value="1")
        fields.append(field)
        
        field = tf.DIV()
        field.label = tf.LABEL(content = 'Username : ', FOR="user_name")
        field.input = tf.INPUT(**{'type':'text', 'id':'user_name', 'name':'user_name', 'data-bind':'value: username'})
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Password : ', FOR="password")
        field.input = tf.INPUT(**{'type':'password', 'id':'password', 'name':'password', 'data-bind':'value: password'})
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Re enter Password : ', FOR='re_password')
        field.input = tf.INPUT(**{'type':'password', 'id':'re_password', 'name':'re_password', 'data-bind':'value: re_password'})
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Email : ', FOR='email')
        field.input = tf.INPUT(**{'type':'email', 'id':'email', 'name':'email', 'data-bind':'value: email'})
        fields.append(field)

        field = tf.DIV()
        field.button = tf.BUTTON("Save", **{'id':'Save-btn', 'data-bind':'click: clicked'})
        fields.append(field)
        
        form  = tf.FORM(id="create_super")
        for field in fields:
            field.line = tf.BR()
            form.content = field
        
        container.form = form
        container.msg = tf.SPAN(id="CreateSuper-msg")
        container.script = tf.SCRIPT(open("fe/src/js/super_create.js").read(), escape=False, type="text/javascript", language="javascript")
        return container
