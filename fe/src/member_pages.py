# -*- coding: UTF-8 -*-

import sphc
import sphc.more
import fe.bases
import pycountry
import commonlib.shared.static_data as data_lists

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
            field.input.option = tf.OPTION(language, value=language)
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL('Country', FOR='country')
        field.input = tf.SELECT(id='country', name='country')
        for country in list(pycountry.countries):
            field.input.option = tf.OPTION(country.name.encode("utf-8"), value=country.name.encode("utf-8"))
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Email', FOR='email')
        field.input = tf.INPUT(type='email', id='email', name='email')
        fields.append(field)

        field = tf.DIV(Class="submit-btns")
        field.button = tf.BUTTON("Create", id='save-btn', type='button')
        fields.append(field)

        form  = tf.FORM(id="createmember_form")
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
        input_type_list = {'Country': [ country.name.encode("utf-8") for country in list(pycountry.countries)]}
        input_type_textarea = ['Address']
        fields = get_editable_fields(field_list, input_type_text, input_type_list, input_type_textarea, [])

        fields.append(make_buttons)

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
            form.content = field

        container.form = form

        input_type_list = {'Theme': data_lists.themes, 'Language': data_lists.languages}
        fields = get_editable_fields(field_list, [], input_type_list, [], [])

        fields.append(make_buttons())

        form  = tf.FORM(Class='profile-forsms', id="preferences_edit_form", style="display:none")
        for field in fields:
            form.content = field

        container.form = form

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
                    field.input_section.input.option = tf.OPTION(ob, value=ob)
        fields.append(field)
    return fields
