import sphc
import fe.bases
import pycountry
import commonlib.shared.static_data as data_lists

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

class MemberCreate(BasePage):
    current_tab = 'create'
    title = 'New Member'
    def  main(self):
        container = tf.DIV()
        
        fields = []

        field = tf.DIV()
        field.label = tf.LABEL(content = 'First Name : ', For="first_name")
        field.input = tf.INPUT(**{'type':'text', 'id':'first_name', 'name':'first_name', 'data-bind':'value: first_name'})
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Last Name : ', FOR="last_name")
        field.input = tf.INPUT(**{'type':'text', 'id':'last_name', 'name':'last_name', 'data-bind':'value: last_name'})
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
        field.label = tf.LABEL('Language : ', FOR='language')
        field.input = tf.SELECT(**{'id':'language', 'name':'language', 'data-bind':'selectedOptions: language'})
        for language in data_lists.languages:
            field.input.option = tf.OPTION(language, value=language)
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL('Country : ', FOR='country')
        field.input = tf.SELECT(**{'id':'country', 'name':'country', 'data-bind':'selectedOptions: country'})
        for country in list(pycountry.countries):
            field.input.option = tf.OPTION(country.name.encode("utf-8"), value=country.name.encode("utf-8"))
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Email : ', FOR='email')
        field.input = tf.INPUT(**{'type':'email', 'id':'email', 'name':'email', 'data-bind':'value: email'})
        fields.append(field)

        field = tf.DIV()
        field.button = tf.BUTTON("Save", **{'id':'Save-btn', 'data-bind':'click: clicked'})
        fields.append(field)
        
        form  = tf.FORM(id="create_member")
        for field in fields:
            field.line = tf.BR()
            form.content = field
        
        container.form = form
        container.msg = tf.SPAN(id="CreateMember-msg")
        container.script = tf.SCRIPT(open("fe/src/js/member_create.js").read(), escape=False, type="text/javascript", language="javascript")
        return container
