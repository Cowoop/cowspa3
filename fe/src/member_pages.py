# -*- coding: UTF-8 -*-

import sphc
import sphc.more
import fe.bases
import commonlib.shared.static as data_lists

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

def make_buttons():
    container = tf.DIV()
    buttons = tf.DIV(Class="buttons")
    buttons.button = tf.BUTTON("Save", id='save-btn', type='button')
    buttons.button = tf.BUTTON("Cancel", id='cancel-btn', type='button')
    container.buttons = buttons
    return container

class MemberCreate(BasePage):
    current_nav = 'Members'
    title = 'New Member'
    def content(self):
        container = tf.DIV()

        fields = []

        field = tf.DIV()
        field.label = tf.LABEL(content = 'First Name', For="first_name")
        field.input = tf.INPUT(type='text', id='first_name', name='first_name')
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Last Name', FOR="last_name")
        field.input = tf.INPUT(type='text', id='last_name', name='last_name')
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Username', FOR="user_name")
        field.input = tf.INPUT(type='text', id='username', name='username')
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Password', FOR="password")
        field.input = tf.INPUT(type='password', id='password', name='password')
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL('Language', FOR='language')
        field.input = tf.SELECT(id='language', name='language')
        for language in data_lists.languages:
            field.input.option = tf.OPTION(language['label'], value=language['name'])
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL('Country', FOR='country')
        field.input = tf.SELECT(id='country', name='country')
        for country in data_lists.countries:
            field.input.option = tf.OPTION(country['label'], value=country['name'])
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Email', FOR='email')
        field.input = tf.INPUT(type='email', id='email', name='email')
        fields.append(field)

        field = tf.DIV(Class="submit-btns")
        field.button = tf.BUTTON("Create", id='save-btn', type='button')
        fields.append(field)

        form  = tf.FORM(Class='profile-forms', id="createmember_form")
        for field in fields:
            form.content = field

        container.form = form
        container.msg = tf.SPAN(id="CreateMember-msg")
        container.script = tf.SCRIPT(open("fe/src/js/member_create.js").read(), escape=False, type="text/javascript", language="javascript")
        return container

class MemberProfile(BasePage):
    current_nav = 'Profile'
    title = 'Profile'
    content_title = ''

    def content(self):

        container = tf.DIV()
        #                                                 About me Form       
        edit = tf.DIV(Class="edit-link-box")
        edit.link = tf.A("Edit", id='edit-link', href='#about')
        fields = [edit]

        field_data = [('First name', 'first_name'),
            ('Last name', 'last_name'),
            ('Short description', 'short_description'),
            ('Long description', 'long_description')]
        for label, name in field_data:
            field = tf.DIV(Class="field-container")
            field.label = tf.DIV(label, Class="field-name")
            field.value = tf.DIV(id=name, Class="field-value")
            fields.append(field)

        view = tf.DIV(Class='profile-forms', id="about_view_form", style="display:none")
        view.fields= fields

        container.view = view

        field_list = ['First_Name','Last_Name','Short_Description','Long_Description','Organization']

        input_type_text = ['First_Name','Last_Name','Organization']
        input_type_textarea = ['Short_Description','Long_Description']
        fields = get_editable_fields(field_list, input_type_text, {}, input_type_textarea, [])

        fields.append(make_buttons())

        form  = tf.FORM(Class='profile-forms', id="about_edit_form", style="display:none")
        for field in fields:
            form.content = field

        container.form = form

        #                                       Account
        fields = []
        field = tf.DIV()
        field.label = tf.LABEL('User Name', FOR='username')
        field.input = tf.INPUT(type='text', id='username', name='username')
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL('Password', FOR='password')
        field.input = tf.INPUT(type='password', id='password', name='password', placeholder="••••••••")
        fields.append(field)

        field = tf.DIV()
        field.button = tf.BUTTON("Save", id='save-btn', type='button')
        fields.append(field)

        form  = tf.FORM(Class='profile-forms', id="account_edit_form", style="display:none")
        for field in fields:
            form.content = field

        container.form = form

        #                                         Social me Form       
        field_list = ['Website', 'Blog', 'Twitter', 'Facebook', 'Linkedin']
        fields = []
        web_links = ['Website', 'Blog', 'Twitter', 'Facebook', 'Linkedin']

        edit = tf.DIV(Class="edit-link-box")
        edit.link = tf.A("Edit", id='edit-link', href='#social')
        fields = [edit]

        fields = get_static_fields(field_list, web_links, fields)

        form  = tf.FORM(Class='profile-forms', id="social_view_form", style="display:none")
        for field in fields:
            form.content = field

        container.form = form

        input_type_text = ['Website', 'Blog', 'Twitter', 'Facebook', 'Linkedin']
        fields = get_editable_fields(field_list, input_type_text, {}, [], [])

        fields.append(make_buttons())

        form  = tf.FORM(Class='profile-forms', id="social_edit_form", style="display:none")
        for field in fields:
            form.content = field

        container.form = form

        ######### Memberships ###################

        tariff_box = tf.DIV(id="memberships_view_form", Class="profile-forms hidden")

        new = tf.DIV(Class="right-action")
        new.button = tf.BUTTON("Next Tariff", id="next_tariff-btn", name="next_tarrif-btn", type="button")

        header = tf.TR()
        header.th = tf.TH("Place")
        header.th = tf.TH("Tariff")
        header.th = tf.TH("Since")
        header.th = tf.TH("Till")
        header.th = tf.TH("Actions")

        tariff_row = sphc.more.jq_tmpl("tariff-row")
        tariff_row.tr = tf.TR(id="tariff_row-${id}")
        tariff_row.tr.td = tf.TD("${bizplace_name}", id="bizplace_name")
        tariff_row.tr.td = tf.TD("${plan_name}", id="plan_name")
        tariff_row.tr.td = tf.TD("${starts}", Class="date", id="starts")
        tariff_row.tr.td = tf.TD("${ends}", Class="date", id="ends")
        cell = tf.TD()
        cell.a = tf.A("Change", href="#change-sub", Class="change-sub", id="change_sub-${id}")
        cell.c = tf.C(" | ")
        cell.a = tf.A('X', title="Cancel tariff", href="#cancel-sub", Class="cancel-sub", id="cancel_sub-${id}")    
        tariff_row.tr.td = cell
        
        tariff_load_history = tf.DIV()
        tariff_load_history.link = tf.A("Load tariff history", id='load-tariff-history', href='#memberships')

        tariff_info = tf.TABLE(id="tariff-info", cellspacing="1em", Class="stripped")
        tariff_info.caption = tf.CAPTION("Manage Tariffs")
        tariff_info.header = header

        tariff_box.new = new
        tariff_box.tmpl = tariff_row
        tariff_box.info = tariff_info
        tariff_box.history = tariff_load_history

        container.tariff_box = tariff_box
        
        tariff_list_row = sphc.more.jq_tmpl("tariff-options")
        tariff_list_row.option = tf.option("${name}", value="${id}")
        
        next_tariff_form = sphc.more.Form(id='next-tariff-form', classes=['vform'])
        next_tariff_form.add_field("Tariff", tf.SELECT(name='tariff', id='tariff'))
        next_tariff_form.add_field("Start", tf.INPUT(name='start', type="date", id='start', nv_attrs=('required')))
        next_tariff_section = tf.DIV(id='next-tariff-section', Class='hidden')
        next_tariff_section.form = next_tariff_form.build()
        next_tariff_section.tmpl = tariff_list_row
        next_tariff_section.form.msg = tf.SPAN(id="Next_Tariff-msg")
        container.next_tarrif = next_tariff_section
        
        change_tariff_form = sphc.more.Form(id='change-tariff-form', classes=['vform'])
        change_tariff_form.add_field("Tariff", tf.SELECT(name='tariff', id='tariff'))
        change_tariff_form.add_field("Start", tf.INPUT(name='start', type="date", id='start'))
        change_tariff_form.add_field("End", tf.INPUT(name='end', type="date", id='end'))
        change_tariff_section = tf.DIV(id='change-tariff-section', Class='hidden')
        change_tariff_section.form = change_tariff_form.build()
        change_tariff_section.tmpl = tariff_list_row
        change_tariff_section.form.msg = tf.SPAN(id="Change_Tariff-msg")
        container.change_tarrif = change_tariff_section

        #                                                Contact Form
        field_list = ['Address', 'City', 'Country', 'Pincode', 'Phone', 'Mobile', 'Fax', 'Email', 'Skype', 'Sip']

        edit = tf.DIV(Class="edit-link-box")
        edit.link = tf.A("Edit", id='edit-link', href='#contact')
        fields = [edit]

        fields = get_static_fields(field_list, [], fields)

        form  = tf.FORM(Class='profile-forms', id="contact_view_form", style="display:none")
        for field in fields:
            form.content = field

        container.form = form

        input_type_text = ['City', 'Pincode', 'Phone', 'Mobile', 'Fax', 'Email', 'Skype', 'Sip']
        input_type_list = {'Country': data_lists.countries}
        input_type_textarea = ['Address']
        fields = get_editable_fields(field_list, input_type_text, input_type_list, input_type_textarea, [])

        fields.append(make_buttons())

        form  = tf.FORM(Class='profile-forms', id="contact_edit_form", style="display:none")
        for field in fields:
            form.content = field

        container.form = form

        #                                                Preferences Form
        field_list = ['Theme', 'Language']

        edit = tf.DIV(Class="edit-link-box")
        edit.link = tf.A("Edit", id='edit-link', href='#preferences')

        fields = [edit]

        fields = get_static_fields(field_list, [], fields)

        form  = tf.FORM(Class='profile-forms', id="preferences_view_form", style="display:none")
        for field in fields:
            form.field = field

        container.form = form

        input_type_list = {'Theme': data_lists.themes, 'Language': data_lists.languages}
        fields = get_editable_fields(field_list, [], input_type_list, [], [])

        fields.append(make_buttons())

        form  = tf.FORM(Class='profile-forms', id="preferences_edit_form", style="display:none")
        for field in fields:
            form.field = field

        container.form = form

        ############################Billing Preferences############################
         
        billing_pref = tf.DIV(id="billing_preferences_section", Class="profile-forms hidden")
        billing_pref_form = tf.form(id="billing_pref")
        
        billing_pref_form.radio = tf.DIV("Billing Mode")
        billing_pref_form.radio.radio1 = tf.DIV(id="radio_field1")
        billing_pref_form.radio.radio1.value = tf.INPUT(id="mode", name="mode", type="radio", value="0")
        billing_pref_form.radio.radio1.label = tf.label("Self")
        billing_pref_form.radio.radio2 = tf.DIV(id="radio_field2")
        billing_pref_form.radio.radio2.value = tf.INPUT(id="mode", name="mode", type="radio", value="1")
        billing_pref_form.radio.radio2.label = tf.label("Bizness")
        billing_pref_form.radio.radio3 = tf.DIV(id="radio_field3")
        billing_pref_form.radio.radio3.value = tf.INPUT(id="mode", name="mode", type="radio", value="2")
        billing_pref_form.radio.radio3.label = tf.label("Another Member")
        
        billing_pref_form.details = tf.DIV("Billing Details")
        
        billing_pref_form.details.self = tf.DIV(id="details_0", Class="hidden")
        billing_pref_form.details.self.radio1 = tf.DIV(id="self_radio_field1")
        billing_pref_form.details.self.radio1.value = tf.INPUT(id="self_mode0", name="self_mode", type="radio", value="0")
        billing_pref_form.details.self.radio1.label = tf.label("Use Profile Details")
        billing_pref_form.details.self.radio2 = tf.DIV(id="self_radio_field2")
        billing_pref_form.details.self.radio2.value = tf.INPUT(id="self_mode1", name="self_mode", type="radio", value="1")
        billing_pref_form.details.self.radio2.label = tf.label("Use Details As Below")
        billing_pref_form.details.self.form = tf.FORM(id="self_details-form")
        billing_pref_form.details.self.form.name = tf.DIV()
        billing_pref_form.details.self.form.name.label = tf.LABEL(content = 'Name', For="self_name")
        billing_pref_form.details.self.form.name.input = tf.INPUT(type='text', id='self_name', name='self_name')        
        billing_pref_form.details.self.form.address = tf.DIV()
        billing_pref_form.details.self.form.address.label = tf.LABEL(content = 'Address', FOR="self_address")
        billing_pref_form.details.self.form.address.input = tf.TEXTAREA(id='self_address', name='self_address')
        billing_pref_form.details.self.form.city = tf.DIV()
        billing_pref_form.details.self.form.city.label = tf.LABEL(content = 'City', FOR="self_city")
        billing_pref_form.details.self.form.city.input = tf.INPUT(id='self_city', name='self_city', type="text")
        billing_pref_form.details.self.form.country = tf.DIV()
        billing_pref_form.details.self.form.country.label = tf.LABEL(content = 'Country', FOR="self_country")
        billing_pref_form.details.self.form.country.input = tf.SELECT(id='self_country', name='self_country')
        for country in data_lists.countries:
                billing_pref_form.details.self.form.country.input.option = tf.OPTION(country['label'], value=country['name'])
        billing_pref_form.details.self.form.phone = tf.DIV()
        billing_pref_form.details.self.form.phone.label = tf.LABEL(content = 'Phone', FOR='self_phone')
        billing_pref_form.details.self.form.phone.input = tf.INPUT(type='text', id='self_phone', name='self_phone')
        billing_pref_form.details.self.form.email = tf.DIV()
        billing_pref_form.details.self.form.email.label = tf.LABEL(content = 'Email', FOR='self_email')
        billing_pref_form.details.self.form.email.input = tf.INPUT(type='email', id='self_email', name='self_email')
        
        billing_pref_form.details.bizness = tf.DIV(id="details_1", Class="hidden")
        billing_pref_form.details.bizness.radio1 = tf.DIV(id="bizness_radio_field1")
        billing_pref_form.details.bizness.radio1.value = tf.INPUT(id="bizness_mode0", name="bizness_mode", type="radio", value="0")
        billing_pref_form.details.bizness.radio1.label = tf.label("Bill To Existing")
        billing_pref_form.details.bizness.radio1.input = tf.INPUT(type="text", id="existing_biz")
        billing_pref_form.details.bizness.radio2 = tf.DIV(id="bizness_radio_field2")
        billing_pref_form.details.bizness.radio2.value = tf.INPUT(id="bizness_mode1", name="bizness_mode", type="radio", value="1")
        billing_pref_form.details.bizness.radio2.label = tf.label("Add New Bizness")
        billing_pref_form.details.bizness.form = tf.FORM(id="new_biz-form")
        billing_pref_form.details.bizness.form.name = tf.DIV()
        billing_pref_form.details.bizness.form.name.label = tf.LABEL(content = 'Bizness Name', For="biz_name")
        billing_pref_form.details.bizness.form.name.input = tf.INPUT(type='text', id='biz_name', name='biz_name')        
        billing_pref_form.details.bizness.form.address = tf.DIV()
        billing_pref_form.details.bizness.form.address.label = tf.LABEL(content = 'Address', FOR="biz_address")
        billing_pref_form.details.bizness.form.address.input = tf.TEXTAREA(id='biz_address', name='biz_address')
        billing_pref_form.details.bizness.form.city = tf.DIV()
        billing_pref_form.details.bizness.form.city.label = tf.LABEL(content = 'City', FOR="biz_city")
        billing_pref_form.details.bizness.form.city.input = tf.INPUT(id='biz_city', name='biz_city', type="text")
        billing_pref_form.details.bizness.form.country = tf.DIV()
        billing_pref_form.details.bizness.form.country.label = tf.LABEL(content = 'Country', FOR="biz_country")
        billing_pref_form.details.bizness.form.country.input = tf.SELECT(id='biz_country', name='biz_country')
        for country in data_lists.countries:
                billing_pref_form.details.bizness.form.country.input.option = tf.OPTION(country['label'], value=country['name'])
        billing_pref_form.details.bizness.form.phone = tf.DIV()
        billing_pref_form.details.bizness.form.phone.label = tf.LABEL(content = 'Phone', FOR='biz_phone')
        billing_pref_form.details.bizness.form.phone.input = tf.INPUT(type='text', id='biz_phone', name='biz_phone')
        billing_pref_form.details.bizness.form.email = tf.DIV()
        billing_pref_form.details.bizness.form.email.label = tf.LABEL(content = 'Email', FOR='biz_email')
        billing_pref_form.details.bizness.form.email.input = tf.INPUT(type='email', id='biz_email', name='biz_email')
        
        billing_pref_form.details.member = tf.DIV(id="details_2", Class="hidden")
        billing_pref_form.details.member.label = tf.LABEL("Bill To Existing Member")
        billing_pref_form.details.member.value = tf.INPUT(id="member", type="text")
        
        billing_pref_form.buttons = tf.DIV(Class="buttons")
        billing_pref_form.buttons.save = tf.INPUT(id="save-billingpref", type="button", value="Save")        
        billing_pref_form.msg = tf.SPAN(id="billing_pref-msg")
        
        billing_pref.form = billing_pref_form
              
        container.billing_pref = billing_pref
    
        container.script = tf.SCRIPT(open("fe/src/js/member_profile.js").read(), escape=False, type="text/javascript", language="javascript")
        container.script = tf.SCRIPT(open("fe/src/js/common_form_methods.js").read(), escape=False, type="text/javascript", language="javascript")
        return container

def get_static_fields(field_list, web_links, fields):
    
    for attr in field_list:
        field = tf.DIV(Class="field-container")
        field.label = tf.DIV(content = ' '.join(attr.split('_')), Class="field-name")
        if attr in web_links:
            field.a = tf.A(id=attr.lower(), name=attr.lower(), href="")
        else:
            field.a = tf.DIV(id=attr.lower(), name=attr.lower(), Class="field-value")
        fields.append(field)
    fields.append(sphc.more.clear())
    return fields

def get_editable_fields(field_list, input_type_text, input_type_list, input_type_textarea, fields):

    for attr in field_list:
        field = tf.DIV()
        field.label = tf.LABEL(' '.join(attr.split('_')), FOR=attr.lower())
        field.input_section = tf.DIV(Class='input-section')
        if attr in input_type_text:
            if attr in ['Twitter', 'Facebook', 'Linkedin']:
                placeholder = 'Eg. My ' + attr
                inputs = [
                    tf.INPUT(type='text', id=attr.lower()+"-label", name=attr.lower()+"-label", placeholder=placeholder),
                    tf.INPUT(type='text', id=attr.lower()+"-url", name=attr.lower()+"-url", placeholder="URL") ]
                field.input_section.inputs = inputs
            else:
                field.input_section.input = tf.INPUT(type='text', id=attr.lower(), name=attr.lower())
        elif attr in input_type_textarea:
            field.input_section.input = tf.TEXTAREA(id=attr.lower(), name=attr.lower(), rows=2, cols=25)
        elif attr in input_type_list:
            field.input_section.input = tf.SELECT(id=attr.lower(), name=attr.lower())
            for ob in input_type_list[attr]:
                field.input_section.input.option = tf.OPTION(ob['label'], value=ob['name'])
        fields.append(field)
    return fields
