import sphc
import fe.bases
import pycountry

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

class BizplaceCreate(BasePage):
    current_tab = 'create'
    title = 'New Bizplace'
    def  main(self):
        container = tf.DIV()

        fields = []

        field = tf.DIV()
        field.label = tf.LABEL('Biz ID : ', FOR='biz_id')
        field.input = tf.SELECT(**{'id':'biz_id', 'name':'biz_id', 'data-bind':'selectedOptions: biz_id'})
        field.input.option = tf.OPTION("1", value="1")
        fields.append(field)
        
        field = tf.DIV()
        field.label = tf.LABEL(content = 'Name : ', For="name")
        field.input = tf.INPUT(**{'type':'text', 'id':'name', 'name':'name', 'data-bind':'value: name'})
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Address : ', FOR="address")
        field.input = tf.INPUT(**{'type':'text', 'id':'address', 'name':'address', 'data-bind':'value: address'})
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'City : ', FOR="city")
        field.input = tf.INPUT(**{'type':'text', 'id':'city', 'name':'city', 'data-bind':'value: city'})
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
        field.label = tf.LABEL(content = 'Short Description : ', FOR="short_desc")
        field.input = tf.TEXTAREA(**{ 'id':'short_desc', 'name':'short_desc', 'rows':2, 'cols':25, 'data-bind':'value: short_desc'})
        fields.append(field)
        
        field = tf.DIV()
        field.button = tf.BUTTON("Save", **{'id':'Save-btn', 'data-bind':'click: clicked'})
        fields.append(field)

        form  = tf.FORM(id="create_bizplace")
        for field in fields:
            field.line = tf.BR()
            form.content = field
         
        container.form = form
        container.msg = tf.SPAN(id="CreateBizplace-msg")
        container.script = tf.SCRIPT(open("fe/src/js/bizplace_create.js").read(), escape=False, type="text/javascript", language="javascript")
        return container 
