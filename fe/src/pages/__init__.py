import sphc
import sphc.more
import fe.bases

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

class LoginPage(fe.bases.CSAnonPage):
    title = "Cowspa | Login"
    def main(self):
        container = tf.DIV(id="login-container")
        formbox = tf.DIV(Class='login-form-box')
        form = sphc.more.Form(id="login-form", classes=['vform'])
        form.add_field('Username', tf.INPUT(type="TEXT", id='username', name="username", placeholder="Username"))
        form.add_field('Password', tf.INPUT(type="password", id='password', name="password", placeholder="Password"))
        form.add_buttons(tf.BUTTON("Log In", id='login-btn', type='button'))
        formbox.form = form.build()
        formbox.form.msg = tf.SPAN(id="login-msg")
        container.formbox = formbox
        container.script = tf.SCRIPT(open("fe/src/js/login.js").read(), escape=False, type="text/javascript")

        container.imgbox = tf.DIV(Class="login-img")
        container.imgbox.img = tf.IMG(src="/images/cow.png")
        #container.clear = sphc.more.clear()
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
        container.ul = tf.UL(id="activities", name="activities")
        container.script = tf.SCRIPT(open("fe/src/js/dashboard.js").read(), escape=False, type="text/javascript", language="javascript")
        return container

class GettingStarted(BasePage):
    current_nav = 'Dashboard'
    title = ''
