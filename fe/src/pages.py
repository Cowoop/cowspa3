import sphc
import fe.bases

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

class LoginPage(fe.bases.CSAnonPage):
    title = "Cowspa | Login"
    def main(self):
        container = tf.DIV()
        username = tf.INPUT(type="TEXT", id='username', name="username", placeholder="Username")
        password = tf.INPUT(type="PASSWORD", id='password', name="password", placeholder="Password")
        submit = tf.BUTTON("Log In", id='login-btn', type="button")
        form = tf.FORM(id="login_form")
        form.fields = [username, password, submit]
        container.form = form
        container.msg = tf.SPAN(id="login-msg")
        container.script = tf.SCRIPT(open("fe/src/js/login.js").read(), escape=False)
        return container

class InvoicingPage(BasePage):
    current_tab = 'invoicing'
    title = 'Invoicing'

    def  main(self):
        return tf.H1("Invoicing")
