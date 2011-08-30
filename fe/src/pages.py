import sphc
import sphc.more
import fe.bases

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

class LoginPage(fe.bases.CSAnonPage):
    title = "Cowspa | Login"
    def main(self):
        container = tf.DIV(Class="login-mainx")
        username = tf.INPUT(type="TEXT", id='username', name="username", placeholder="Username")
        password = tf.INPUT(type="PASSWORD", id='password', name="password", placeholder="Password")
        submit = tf.BUTTON("Log In", id='login-btn', type='button')
        formbox = tf.DIV(Class="login-form-box")
        form = tf.FORM(id = "login_form")
        form.fields = [username, password, submit]
        container.formbox = formbox
        container.formbox.form = form
        container.msg = tf.SPAN(id="login-msg")
        container.script = tf.SCRIPT(open("fe/src/js/login.js").read(), escape=False, type="text/javascript")

        container.imgbox = tf.DIV(Class="login-img")
        container.imgbox.img = tf.IMG(src="/images/cow.png", width="50%%", height="50%%", align="left")
        container.clear = sphc.more.clear()
        return container

class LogoutPage(fe.bases.CSAnonPage):
    title = "Cowspa | Logout"
    def main(self):
        return tf.SCRIPT(open("fe/src/js/logout.js").read(), escape=False, type="text/javascript", language="javascript")

class InvoicingPage(BasePage):
    current_tab = 'invoicing'
    title = 'Invoicing'

    def  main(self):
        return tf.H1("Invoicing")

class Dashboard(BasePage):
    current_nav = 'Dashboard'
    title = 'Host Dashboard'

    def content(self):
        container = tf.DIV()
        container.h2 = tf.H2("Welcome")
        container.ul = tf.UL(id="activities", name="activities")
        container.script = tf.SCRIPT(open("fe/src/js/dashboard.js").read(), escape=False, type="text/javascript", language="javascript")
        return container

class SuperuserCreate(fe.bases.CSAnonPage):
    current_tab = 'create'
    title = 'New Super User'
    def main(self):
        container = tf.DIV()

        fields = []

        field = tf.DIV()
        field.label = tf.LABEL(content = 'First Name : ', For="first_name")
        field.input = tf.INPUT('required', type='text', id='first_name', name='first_name')
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Username : ', FOR="username")
        field.input = tf.INPUT(type='text', id='username', name='username')
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Password : ', FOR="password")
        field.input = tf.INPUT(type='password', id='password', name='password')
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Email : ', FOR='email')
        field.input = tf.INPUT(type='email', id='email', name='email')
        fields.append(field)

        field = tf.DIV()
        field.button = tf.BUTTON("Create", id='save-btn', type='button')
        fields.append(field)

        form  = tf.FORM(id="createsuper_form")
        for field in fields:
            field.line = tf.BR()
            form.content = field

        container.form = form
        container.msg = tf.SPAN(id="CreateSuper-msg")
        container.script = tf.SCRIPT(open("fe/src/js/super_create.js").read(), escape=False, type="text/javascript", language="javascript")
        return container
