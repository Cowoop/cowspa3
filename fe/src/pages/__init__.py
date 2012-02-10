import sphc
import sphc.more
import fe.bases
import fe.src.forms as forms

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

class Login(fe.bases.CSAnonPage):
    title = "Cowspa | Login"
    def main(self):
        container = tf.DIV(id="login-main-container")
        container.side_container = tf.DIV(id="login-side-container")

        formbox = tf.DIV(Class='inverse-box')
        form = sphc.more.Form(id="login-form", classes=['vform'])
        form.add_field('', tf.INPUT(type="TEXT", id='username', name="username", placeholder="Username", nv_attrs=('required',)))
        form.add_field('', tf.INPUT(type="password", id='password', name="password", placeholder="Password"))
        form.add_buttons(tf.BUTTON("Log In", id='login-btn', type='submit'))
        formbox.form = form.build()

        container.side_container.formbox = formbox
        # Signup code // begin
        #container.side_container.register_link = tf.DIV("Signing up is quick and easy", Class="inverse-box")
        #container.side_container.register_link.a = tf.BUTTON('Signup', href='#', id="signup-btn")

        #signup_box = tf.DIV(id='signup-box', Class="hidden inverse-box")
        #signup_box.form = forms.signup_form().build()
        #container.signup_box = signup_box
        # Signup code // end

        container.imgbox = tf.DIV(Class="login-img")
        container.imgbox.img = tf.IMG(src="/images/cow.png")
        #container.clear = sphc.more.clear()
        container.script = tf.SCRIPT(open("fe/src/js/login.js").read(), escape=False, type="text/javascript")
        return container

class Activation(fe.bases.CSAnonPage):
    title = "Cowspa | Activation"
    def main(self):
        container = tf.DIV(id="login-main-container")
        container.side_container = tf.DIV(id="login-side-container")

        formbox = tf.DIV(Class='inverse-box')
        form = sphc.more.Form(id="login-form", classes=['vform'])
        form.add_field('', tf.INPUT(type="TEXT", id='username', name="username", placeholder="Choose a username"))
        form.add_field('', tf.INPUT(type="password", id='password', name="password", placeholder="Choose a password"))
        form.add_buttons(tf.BUTTON("Complete account activation", id='login-btn', type='button'))
        formbox.form = form.build()

        container.side_container.formbox = formbox

        container.imgbox = tf.DIV(Class="login-img")
        container.imgbox.img = tf.IMG(src="/images/cow.png")
        #container.clear = sphc.more.clear()
        container.script = tf.SCRIPT(open("fe/src/js/activate.js").read(), escape=False, type="text/javascript")
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
        container.activities_pane = tf.UL(id="activities", name="activities")
        container.script = tf.SCRIPT(open("fe/src/js/dashboard.js").read(), escape=False, type="text/javascript", language="javascript")
        return container

    def sidebar(self):
        content = tf.DIV(tf.DIV("Getting started", Class="title"))
        content.action = [tf.BR(), tf.A("Add your " + __("Coworking Place"), href="/${lang}/${theme}/bizplace/new", Class="big-button")]
        return content

class GettingStarted(BasePage):
    current_nav = 'Dashboard'
    title = ''
