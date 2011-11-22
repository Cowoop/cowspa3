# -*- coding: UTF-8 -*-

import sphc
import sphc.more
import fe.bases
import fe.src.common
import commonlib.shared.static as data_lists
import commonlib.shared.symbols

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

def contact_form():
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
    return form

def account_form():
    form = sphc.more.Form(id='member-account-edit', Class='profile-edit-form', classes=['hform'])
    form.add_field("Username", tf.INPUT(type='text', id='username', name='username'))
    form.add_field("Password", tf.INPUT(type='password', id='password', name='password', placeholder="••••••••"))
    form.add_buttons(tf.BUTTON("Update", type="submit"))
    return form

def preferences_form():
    form = sphc.more.Form(id='member-preferences-edit', Class='profile-edit-form', classes=['hform'])
    themes = tf.SELECT(id="theme", name="theme")
    for ob in data_lists.themes:
        themes.option = tf.OPTION(ob['label'], value=ob['name'])
    form.add_field("Theme", themes)
    languages = tf.SELECT(id="language", name="language")
    for ob in data_lists.languages:
        languages.option = tf.OPTION(ob['label'], value=ob['name'])
    form.add_field("Languages", languages)
    form.add_buttons(tf.BUTTON("Update", type="submit"))
    return form

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
    billing_pref_form.mode.radio4.label = tf.label("Organization")
    
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
    
    billing_pref_form.details.organization = tf.DIV(id="details_3", Class="hidden")
    billing_pref_form.details.organization.radio1 = tf.DIV(id="organization_radio_field1")
    billing_pref_form.details.organization.radio1.value = tf.INPUT(id="organization_mode0", name="organization_mode", type="radio", value="0")
    billing_pref_form.details.organization.radio1.label = tf.label("Bill To Existing")
    billing_pref_form.details.organization.radio1.input = tf.INPUT(type="text", id="existing_org")
    billing_pref_form.details.organization.radio2 = tf.DIV(id="organization_radio_field2")
    billing_pref_form.details.organization.radio2.value = tf.INPUT(id="organization_mode1", name="organization_mode", type="radio", value="1")
    billing_pref_form.details.organization.radio2.label = tf.label("Add New Organization")
    billing_pref_form.details.organization.form = tf.FORM(id="new_org-form")
    billing_pref_form.details.organization.form.name = tf.DIV()
    billing_pref_form.details.organization.form.name.label = tf.LABEL(content = 'Organization Name', For="org_name")
    billing_pref_form.details.organization.form.name.input = tf.INPUT(type='text', id='org_name', name='org_name')        
    billing_pref_form.details.organization.form.address = tf.DIV()
    billing_pref_form.details.organization.form.address.label = tf.LABEL(content = 'Address', FOR="org_address")
    billing_pref_form.details.organization.form.address.input = tf.TEXTAREA(id='org_address', name='org_address')
    billing_pref_form.details.organization.form.city = tf.DIV()
    billing_pref_form.details.organization.form.city.label = tf.LABEL(content = 'City', FOR="org_city")
    billing_pref_form.details.organization.form.city.input = tf.INPUT(id='org_city', name='org_city', type="text")
    billing_pref_form.details.organization.form.country = tf.DIV()
    billing_pref_form.details.organization.form.country.label = tf.LABEL(content = 'Country', FOR="org_country")
    billing_pref_form.details.organization.form.country.input = tf.SELECT(id='org_country', name='org_country')
    billing_pref_form.details.organization.form.country.input.options = fe.src.common.country_options
    billing_pref_form.details.organization.form.phone = tf.DIV()
    billing_pref_form.details.organization.form.phone.label = tf.LABEL(content = 'Phone', FOR='org_phone')
    billing_pref_form.details.organization.form.phone.input = tf.INPUT(type='text', id='org_phone', name='org_phone')
    billing_pref_form.details.organization.form.email = tf.DIV()
    billing_pref_form.details.organization.form.email.label = tf.LABEL(content = 'Email', FOR='org_email')
    billing_pref_form.details.organization.form.email.input = tf.INPUT(type='email', id='org_email', name='org_email')
    
    billing_pref_form.msg = tf.SPAN(id="billing_pref-msg")
    
    billing_pref_form.buttons = tf.DIV(Class="buttons")
    billing_pref_form.buttons.update = tf.INPUT(id="update-billingpref", type="button", value="Update")

    return billing_pref_form

def add_tariffs_section(container):
    tariff_box = tf.DIV()

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
    tariff_row.tr.td = tf.TD("${tariff_name}", id="tariff_name")
    tariff_row.tr.td = tf.TD("${starts}", Class="date", id="starts")
    tariff_row.tr.td = tf.TD("${ends}", Class="date", id="ends")
    cell = tf.TD()
    cell.a = tf.A("Change", href="#memberships", Class="change-sub", id="change_sub-${id}")
    cell.c = tf.C(" | ")
    cell.a = tf.A('X', title="Cancel tariff", href="#cancel-sub", Class="cancel-sub", id="cancel_sub-${id}")    
    tariff_row.tr.td = cell
    
    tariff_load_history = tf.DIV()
    tariff_load_history.link = tf.A("Load tariff history", id='load-tariff-history', href='#memberships')

    tariff_info = tf.TABLE(id="tariff-info", cellspacing="1em", Class="stripped")
    tariff_info.caption = tf.CAPTION("Current Tariffs")
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
    next_tariff_form.add_field("", tf.INPUT(id='start', type="hidden"))
    next_tariff_form.add_field("Start", tf.INPUT(name='start-vis', id='start-vis').set_required())
    next_tariff_section = tf.DIV(id='next-tariff-section', Class='hidden')
    next_tariff_section.form = next_tariff_form.build()
    next_tariff_section.tmpl = tariff_list_row
    next_tariff_section.form.msg = tf.SPAN(id="Next_Tariff-msg")
    container.next_tarrif = next_tariff_section
    
    change_tariff_form = sphc.more.Form(id='change-tariff-form', classes=['vform'])
    change_tariff_form.add_field("Tariff", tf.SELECT(name='tariff', id='tariff'))
    change_tariff_form.add_field("", tf.INPUT(type="hidden", id='starts'))
    change_tariff_form.add_field("Start", tf.INPUT(name='starts-vis', id='starts-vis'))
    change_tariff_form.add_field("", tf.INPUT(type="hidden", id='ends'))
    change_tariff_form.add_field("End", tf.INPUT(name='ends-vis', id='ends-vis'))
    change_tariff_section = tf.DIV(id='change-tariff-section', Class='hidden')
    change_tariff_section.form = change_tariff_form.build()
    change_tariff_section.tmpl = tariff_list_row
    change_tariff_section.form.msg = tf.SPAN(id="Change_Tariff-msg")
    container.change_tarrif = change_tariff_section

def make_buttons():
    container = tf.DIV()
    buttons = tf.DIV(Class="buttons")
    buttons.button = tf.BUTTON("Save", id='save-btn', type='submit')
    buttons.button = tf.BUTTON("Cancel", id='cancel-btn', type='button')
    container.buttons = buttons
    return container

class MemberCreate(BasePage):
    current_nav = 'Members'
    title = 'New Member'
    def content(self):
        container = tf.DIV()

        form  = tf.FORM(Class='hform simple-hform', id="createmember_form", method="POST")

        sections = []

        section = tf.FIELDSET()
        section.legend = tf.LEGEND("About")
        section.label = tf.LABEL(content = 'First Name', For="first_name")
        section.input = tf.INPUT(type='text', id='first_name', name='first_name').set_required()

        section.label = tf.LABEL(content = 'Last Name', FOR="last_name")
        section.input = tf.INPUT(type='text', id='last_name', name='last_name')

        section.label = tf.LABEL(content = 'Username', FOR="user_name")
        section.input = tf.INPUT(type='text', id='username', name='username').set_required()

        section.label = tf.LABEL(content = 'Password', FOR="password")
        section.input = tf.INPUT(type='password', id='password', name='password').set_required()

        section.label = tf.LABEL('Language', FOR='language')
        section.lang = tf.SELECT(id='language', name='language')
        section.lang.options = [tf.OPTION(language['label'], value=language['name']) for language in data_lists.languages]

        sections.append(section)

        section = tf.FIELDSET()
        section.legend = tf.LEGEND("Contact")

        section.fields = contact_form().fields

        #section.label = tf.LABEL('Country', FOR='country')
        #section.input = tf.SELECT(id='country', name='country')
        #section.input.options = fe.src.common.country_options
        #section.label = tf.LABEL(content = 'Email', FOR='email')
        #section.input = tf.INPUT(type='email', id='email', name='email').set_required()

        sections.append(section)

        form.sections = sections
        form.status = tf.DIV(Class="action-status")
        #field = tf.DIV(Class="submit-btns")
        form.button = tf.BUTTON("Create", id='save-btn', type='submit')

        container.form = form
        container.script = tf.SCRIPT(open("fe/src/js/member_create.js").read(), escape=False, type="text/javascript", language="javascript")

        return container

class EditProfile(BasePage):
    current_nav = 'Members'
    title = ''
    content_title = ''

    def content(self):
        container = tf.DIV()

        # Profile
        profile = tf.DIV(id="profile")
        profile.info = tf.DIV(id="member-info", Class="labeled-list hidden")
        profile.info.id = [tf.DIV("Membership id", Class="label"), tf.C(Class="data-id")]
        profile.info.username = tf.DIV([tf.DIV("Username", Class="label"), tf.C(Class="data-username")])
        profile.info.email = tf.DIV([tf.DIV("Email", Class="label"), tf.A(href="", Class="data-email-link")])
        profile.info.line = tf.hr(Class="light")

        # About
        profile.about = tf.FIELDSET()
        profile.about.legend = tf.LEGEND("About")
        profile.about.about_div = tf.DIV(id="about")
        form = sphc.more.Form(id='member-about-edit', Class='profile-edit-form', classes=['hform'])
        form.add_field("First Name", tf.INPUT(name='first_name', type="text").set_required())
        form.add_field("Last Name", tf.INPUT(name='last_name', type="text"))
        form.add_field("Short description", tf.INPUT(name='short_description', type="text"))
        form.add_field("Long description", tf.TEXTAREA(name='long_description', type="text"))
        form.add_buttons(tf.BUTTON("Update", type="submit"))
        profile.about.about_div.form = form.build()

        # Account
        profile.account = tf.FIELDSET()
        profile.account.legend = tf.LEGEND("Account")
        profile.account.account_div = tf.DIV(id="account")
        profile.account.account_div.form = account_form().build()
                
        # Contact
        profile.contact = tf.FIELDSET()
        profile.contact.legend = tf.LEGEND("Contact")
        profile.contact.contact_div = tf.DIV(id="contact")
        profile.contact.contact_div.form = contact_form().build()

        # Preferences
        profile.preferences = tf.FIELDSET()
        profile.preferences.legend = tf.LEGEND("Preferences")
        profile.preferences.preferences_div = tf.DIV(id="preferences")
        profile.preferences.preferences_div.form = preferences_form().build()
        
        # Billing
        billing = tf.DIV(id="billing")
        billing.form = billing_pref_form()

        # Memberships
        memberships = tf.DIV(id="memberships")
        add_tariffs_section(memberships) 
        
        # Usages
        usages = tf.DIV(id="usages")
        add_usage = tf.FIELDSET()
        add_usage.legend = tf.LEGEND("Add Usage")
        add_usage_form = sphc.more.Form(id='add-usage-form', action='#', Class='profile-edit-form', classes=['hform'])
        add_usage_form.add_field("Resource Name", tf.SELECT(id="resource_select", name="resource_select"), tf.INPUT(name='resource_name', id='resource_name', placeholder="Resource name").set_required())
        add_usage_form.add_field("Quantity", tf.INPUT(name='quantity', id='quantity', nv_attrs=('required',), placeholder="eg. 10. Not applicable for time based resource"), fhelp="For non time based resources. Do not include unit")
        add_usage_form.add_field("Start", tf.INPUT(name='start_time', id='start_time', nv_attrs=('required',)))
        add_usage_form.add_field("End", tf.INPUT(name='end_time', id='end_time'), "Optional. Only for time based resources.")
        add_usage_form.add_field("Cost", tf.INPUT(name='cost', id='cost'))
        add_usage_form.add_buttons(tf.INPUT(id="calculate_cost-btn", type="Button", value="Calculate Cost", Class="big-button"), '→', tf.INPUT(type="button", value="Add", id='submit-usage', Class="big-button", disabled="disabled"))
        add_usage.form = add_usage_form.build()
        usages.add_usage = add_usage
        usages.resource_select_tmpl = sphc.more.jq_tmpl("resource-tmpl")
        usages.resource_select_tmpl.option = tf.OPTION("${name}", id="resource_${id}", value="${id}")
        
        uninvoiced = tf.FIELDSET()
        uninvoiced.legend = tf.LEGEND("Uninvoiced Usages")
        uninvoiced.table = tf.TABLE(id="usage_table")
        usages.uninvoiced = uninvoiced
        
        #Invoices
        invoices = tf.DIV(id="invoices")
        invoice_history = tf.FIELDSET()
        invoice_history.legend = tf.LEGEND("Invoice History")
        invoice_history.table = tf.TABLE(id="history_table")
        invoice_history.view_invoice_dialog = tf.DIV(id="view_invoice_window", Class='hidden')
        invoice_history.view_invoice_dialog.frame = tf.IFRAME(id="invoice-iframe", src="#", width="800", height="600")
        invoices.table = invoice_history
        
        # Profile Tabs
        container.tabs = tf.DIV(id="profile_tabs")
        container.tabs.list = tf.UL()
        container.tabs.list.tab1 = tf.li(tf.A("Profile", href="#profile"))
        container.tabs.list.tab2 = tf.li(tf.A("Memberships", href="#memberships"))
        container.tabs.list.tab3 = tf.li(tf.A("Billing Preferences", href="#billing"))
        container.tabs.list.tab4 = tf.li(tf.A("Usages", href="#usages"))
        container.tabs.list.tab5 = tf.li(tf.A("Invoices", href="#invoices"))
        container.tabs.profile = profile
        container.tabs.memberships = memberships
        container.tabs.billing = billing
        container.tabs.usages = usages
        container.tabs.invoices = invoices

        container.script = sphc.more.script_fromfile("fe/src/js/member_edit.js")

        return container

