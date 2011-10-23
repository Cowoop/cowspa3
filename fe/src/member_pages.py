# -*- coding: UTF-8 -*-

import sphc
import sphc.more
import fe.bases
import fe.src.common
import commonlib.shared.static as data_lists
import commonlib.shared.symbols

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

def billing_pref_form():
    billing_pref_form = tf.form(id="billing_pref", Class="simple-hform")
    
    billing_pref_form.mode = tf.FIELDSET()
    billing_pref_form.mode.legend = tf.LEGEND("Billing mode")
    billing_pref_form.mode.radio1 = tf.DIV(id="radio_field1")
    billing_pref_form.mode.radio1.value = tf.INPUT(id="mode", name="mode", type="radio", value="0")
    billing_pref_form.mode.radio1.label = tf.label("Profile")
    billing_pref_form.mode.radio2 = tf.DIV(id="radio_field2")
    billing_pref_form.mode.radio2.value = tf.INPUT(id="mode", name="mode", type="radio", value="1")
    billing_pref_form.mode.radio2.label = tf.label("Use custom billing details")
    billing_pref_form.mode.radio3 = tf.DIV(id="radio_field3")
    billing_pref_form.mode.radio3.value = tf.INPUT(id="mode", name="mode", type="radio", value="2")
    billing_pref_form.mode.radio3.label = tf.label("Another Member")
    billing_pref_form.mode.radio4 = tf.DIV(id="radio_field4")
    billing_pref_form.mode.radio4.value = tf.INPUT(id="mode", name="mode", type="radio", value="3")
    billing_pref_form.mode.radio4.label = tf.label("Business")
    
    billing_pref_form.details = tf.FIELDSET()
    
    billing_pref_form.details.legend = tf.LEGEND("Billing Details")
    
    billing_pref_form.details.custom = tf.DIV(id="details_1", Class="hidden")
    billing_pref_form.details.custom.form = tf.FORM(id="custom_details-form")
    billing_pref_form.details.custom.form.name = tf.DIV()
    billing_pref_form.details.custom.form.name.label = tf.LABEL(content = 'Name', For="custom_name")
    billing_pref_form.details.custom.form.name.input = tf.INPUT(type='text', id='custom_name', name='custom_name')        
    billing_pref_form.details.custom.form.address = tf.DIV()
    billing_pref_form.details.custom.form.address.label = tf.LABEL(content = 'Address', FOR="custom_address")
    billing_pref_form.details.custom.form.address.input = tf.TEXTAREA(id='custom_address', name='custom_address')
    billing_pref_form.details.custom.form.city = tf.DIV()
    billing_pref_form.details.custom.form.city.label = tf.LABEL(content = 'City', FOR="self_city")
    billing_pref_form.details.custom.form.city.input = tf.INPUT(id='custom_city', name='custom_city', type="text")
    billing_pref_form.details.custom.form.country = tf.DIV()
    billing_pref_form.details.custom.form.country.label = tf.LABEL(content = 'Country', FOR="custom_country")
    billing_pref_form.details.custom.form.country.input = tf.SELECT(id='custom_country', name='custom_country')
    billing_pref_form.details.custom.form.country.input.options = fe.src.common.country_options
    billing_pref_form.details.custom.form.phone = tf.DIV()
    billing_pref_form.details.custom.form.phone.label = tf.LABEL(content = 'Phone', FOR='custom_phone')
    billing_pref_form.details.custom.form.phone.input = tf.INPUT(type='text', id='custom_phone', name='custom_phone')
    billing_pref_form.details.custom.form.email = tf.DIV()
    billing_pref_form.details.custom.form.email.label = tf.LABEL(content = 'Email', FOR='custom_email')
    billing_pref_form.details.custom.form.email.input = tf.INPUT(type='email', id='custom_email', name='custom_email')
    
    billing_pref_form.details.member = tf.DIV(id="details_2", Class="hidden")
    billing_pref_form.details.member.label = tf.LABEL("Bill To Existing Member")
    billing_pref_form.details.member.value = tf.INPUT(id="member", type="text")
    
    billing_pref_form.details.bizness = tf.DIV(id="details_3", Class="hidden")
    billing_pref_form.details.bizness.radio1 = tf.DIV(id="bizness_radio_field1")
    billing_pref_form.details.bizness.radio1.value = tf.INPUT(id="bizness_mode0", name="bizness_mode", type="radio", value="0")
    billing_pref_form.details.bizness.radio1.label = tf.label("Bill To Existing")
    billing_pref_form.details.bizness.radio1.input = tf.INPUT(type="text", id="existing_biz")
    billing_pref_form.details.bizness.radio2 = tf.DIV(id="bizness_radio_field2")
    billing_pref_form.details.bizness.radio2.value = tf.INPUT(id="bizness_mode1", name="bizness_mode", type="radio", value="1")
    billing_pref_form.details.bizness.radio2.label = tf.label("Add New Business")
    billing_pref_form.details.bizness.form = tf.FORM(id="new_biz-form")
    billing_pref_form.details.bizness.form.name = tf.DIV()
    billing_pref_form.details.bizness.form.name.label = tf.LABEL(content = 'Business Name', For="biz_name")
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
    billing_pref_form.details.bizness.form.country.input.options = fe.src.common.country_options
    billing_pref_form.details.bizness.form.phone = tf.DIV()
    billing_pref_form.details.bizness.form.phone.label = tf.LABEL(content = 'Phone', FOR='biz_phone')
    billing_pref_form.details.bizness.form.phone.input = tf.INPUT(type='text', id='biz_phone', name='biz_phone')
    billing_pref_form.details.bizness.form.email = tf.DIV()
    billing_pref_form.details.bizness.form.email.label = tf.LABEL(content = 'Email', FOR='biz_email')
    billing_pref_form.details.bizness.form.email.input = tf.INPUT(type='email', id='biz_email', name='biz_email')
    
    billing_pref_form.msg = tf.SPAN(id="billing_pref-msg")
    
    billing_pref_form.buttons = tf.DIV(Class="buttons")
    billing_pref_form.buttons.save = tf.INPUT(id="save-billingpref", type="button", value="Save")
    billing_pref_form.buttons.save = tf.INPUT(id="cancel-billingpref", type="button", value="Cancel")

    return billing_pref_form

def add_tariffs_section(container):
    tariff_box = tf.DIV(id="memberships_view_form", Class="profile-forms", style="display:none")

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
    next_tariff_form.add_field("Start", tf.INPUT(name='start', type="date", id='start').set_required())
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
        field.input = tf.INPUT(type='text', id='first_name', name='first_name').set_required()
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Last Name', FOR="last_name")
        field.input = tf.INPUT(type='text', id='last_name', name='last_name')
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Username', FOR="user_name")
        field.input = tf.INPUT(type='text', id='username', name='username').set_required()
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Password', FOR="password")
        field.input = tf.INPUT(type='password', id='password', name='password').set_required()
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
        field.input.options = fe.src.common.country_options
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Email', FOR='email')
        field.input = tf.INPUT(type='email', id='email', name='email').set_required()
        fields.append(field)

        fields.append(tf.DIV(id="CreateMember-msg"))
        field = tf.DIV(Class="submit-btns")
        field.button = tf.BUTTON("Create", id='save-btn', type='submit')
        fields.append(field)

        form  = tf.FORM(Class='profile-forms', id="createmember_form", method="POST")
        form.fields = fields

        container.form = form
        container.script = tf.SCRIPT(open("fe/src/js/member_create.js").read(), escape=False, type="text/javascript", language="javascript")
        return container

class EditProfile(BasePage):
    current_nav = 'Members'
    title = ''
    content_title = ''

    def search(self):
        return ''

    def content(self):
        container = tf.DIV()

        container.search_box = tf.DIV(Class="select-member")
        container.search_box.step = tf.C(commonlib.shared.symbols.circled_nums.one, Class="heading3")
        container.search_box.label = tf.SPAN(tf.LABEL("Select member", For="member-search"))
        container.search_box.cell = tf.SPAN(tf.INPUT(id="member-search", type="text"), Class="search-input")
        container.clear = tf.hr(Class="light")
        #container.title = tf.DIV([tf.c(id="content-title"), tf.SPAN(id="content-subtitle")], Class="content-title")

        # About
        container.title = tf.DIV(tf.A("About", href="#", id="st-about"), Class="section-title")
        container.about_div = tf.DIV(Class="mp-section", id="mp-about")

        form = sphc.more.Form(id='member-about-edit', Class='profile-edit-form', classes=['hform'])
        form.add_field("First Name", tf.INPUT(name='first_name', type="text").set_required())
        form.add_field("Last Name", tf.INPUT(name='last_name', type="text"))
        form.add_field("Short description", tf.INPUT(name='short_description', type="text"))
        form.add_field("Long description", tf.TEXTAREA(name='long_description', type="text"))
        form.add_buttons(tf.BUTTON("Update", type="submit"))

        container.about_div.form = form.build()

        # Contact
        container.title = tf.DIV(tf.A("Contact", href="#", id="st-contact"), Class="section-title")
        container.contact_div = tf.DIV(Class="mp-section", id="mp-contact")

        form = sphc.more.Form(id='member-contact-edit', Class='profile-edit-form', classes=['hform'])
        form.add_field("Address", tf.TEXTAREA(name='address', type="text"))
        form.add_field("City", tf.INPUT(name='city', type="text"))
        select = tf.SELECT(id='country', name='country')
        select.options = fe.src.common.country_options
        form.add_field("Country", select)
        form.add_field("Pincode/Zip", tf.INPUT(name='pincode', type="text"))
        form.add_field("Phone", tf.INPUT(name='phone', type="text"))
        form.add_field("Mobile", tf.INPUT(name='mobile', type="text"))
        form.add_field("Fax", tf.INPUT(name='mobile', type="text"))
        form.add_field("Email", tf.INPUT(name='email', type="email").set_required())
        form.add_field("Skype", tf.INPUT(name='skype', type="text"))
        form.add_field("Sip", tf.INPUT(name='sip', type="text"))
        form.add_buttons(tf.BUTTON("Update", type="submit"))

        container.contact_div.form = form.build()

        # Billing
        container.title = tf.DIV(tf.A("Billing", href="#", id="st-billing"), Class="section-title")
        container.billing_div = tf.DIV(Class="mp-section", id="mp-billing")

        container.billing_div.form = billing_pref_form()

        preferences_div = tf.DIV(Class="mp-section", id="mp-pref")
        social_div = tf.DIV(Class="mp-section", id="mp-social")
        account_div = tf.DIV(Class="mp-section", id="mp-account")

        # Memberships

        container.title = tf.DIV(tf.A("Memberships", href="#", id="st-memberships"), Class="section-title")
        container.memberships_div = tf.DIV(Class="mp-section", id="mp-memberships")
        add_tariffs_section(container.memberships_div)

        container.script = sphc.more.script_fromfile("fe/src/js/common_form_methods.js")
        container.script = sphc.more.script_fromfile("fe/src/js/member_profile.js")
        container.script = sphc.more.script_fromfile("fe/src/js/member_edit.js")

        return container

class MemberProfile(BasePage):
    current_nav = 'My Profile'
    title = 'My Profile'
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

        add_tariffs_section(container)

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
         
        billing_pref_view = tf.DIV(id="billing_preferences_view_section", Class="profile-forms hidden")
        billing_pref_view.edit = tf.DIV(Class="edit-link-box")
        billing_pref_view.edit.link = tf.A("Edit", id='edit-link', href='#billingpreferences')
        billing_pref_view.name = tf.DIV(Class="field-container")
        billing_pref_view.name.label = tf.DIV(content = 'Name', Class="field-name")
        billing_pref_view.name.a = tf.DIV(id='bill_name', name='bill_name', Class="field-value")
        billing_pref_view.address = tf.DIV(Class="field-container")
        billing_pref_view.address.label = tf.DIV(content = 'Address', Class="field-name")
        billing_pref_view.address.a = tf.DIV(id='bill_address', name='bill_address', Class="field-value")
        billing_pref_view.city = tf.DIV(Class="field-container")
        billing_pref_view.city.label = tf.DIV(content = 'City', Class="field-name")
        billing_pref_view.city.a = tf.DIV(id='bill_city', name='bill_city', Class="field-value")
        billing_pref_view.country = tf.DIV(Class="field-container")
        billing_pref_view.country.label = tf.DIV(content = 'Country', Class="field-name")
        billing_pref_view.country.a = tf.DIV(id='bill_country', name='bill_country', Class="field-value")
        billing_pref_view.phone = tf.DIV(Class="field-container")
        billing_pref_view.phone.label = tf.DIV(content = 'Phone', Class="field-name")
        billing_pref_view.phone.a = tf.DIV(id='bill_phone', name='bill_phone', Class="field-value")
        billing_pref_view.email = tf.DIV(Class="field-container")
        billing_pref_view.email.label = tf.DIV(content = 'Email', Class="field-name")
        billing_pref_view.email.a = tf.DIV(id='bill_email', name='bill_email', Class="field-value")
        container.billing_pref_view = billing_pref_view
        
        billing_pref = tf.DIV(id="billing_preferences_edit_section", Class="profile-forms hidden")
        
        billing_pref.form = billing_pref_form()
              
        container.billing_pref = billing_pref
    
        container.script = sphc.more.script_fromfile("fe/src/js/common_form_methods.js")
        container.script = sphc.more.script_fromfile("fe/src/js/member_profile.js")
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
