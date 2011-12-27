import sphc
import sphc.more

tf = sphc.TagFactory()

def signup_form():
    form = sphc.more.Form(id="signup-form", classes=['vform'])
    form.add_field('First name',
        tf.INPUT(required=True, type="TEXT", name="first_name", placeholder="First Name", id="first_name", nv_attrs=('required',)))
    form.add_field('Last name', \
        tf.INPUT(required=True, type="TEXT", name="last_name", placeholder="Last Name", id="last_name", nv_attrs=('required',)))
    form.add_field('Email', tf.INPUT(required=True, type="email", name="email", placeholder="Email Address", id="email", \
        nv_attrs=('required',)))
    form.add_buttons(tf.BUTTON("Email Activation Link", id='register-btn', type='submit'))
    return form
