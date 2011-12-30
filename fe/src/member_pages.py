# -*- coding: UTF-8 -*-

import sphc
import sphc.more
import fe.bases
import fe.src.common
import fe.src.forms
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
    form.add_field("Zipcode", tf.INPUT(name='pincode', type="text"))
    form.add_field("Phone", tf.INPUT(name='phone', type="text"))
    form.add_field("Mobile", tf.INPUT(name='mobile', type="text"))
    form.add_field("Fax", tf.INPUT(name='mobile', type="text"))
    form.add_field("Email", tf.INPUT(name='email', type="email").set_required())
    form.add_field("Skype", tf.INPUT(name='skype', type="text"))
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
    form.add_field("Language", languages)
    form.add_buttons(tf.BUTTON("Update", type="submit"))
    return form

def billing_pref_form():
    billing_pref_form = sphc.more.Form(id="billing_pref", Class="hform")

    mode = billing_pref_form.add(sphc.more.Fieldset())
    mode.add(tf.LEGEND("Billing mode"))
    radio1 = tf.DIV(id="radio_field1")
    radio1.value = tf.INPUT(id="mode", name="mode", type="radio", value="0")
    radio1.label = tf.label("Profile")
    mode.add(radio1)
    radio2 = tf.DIV(id="radio_field2")
    radio2.value = tf.INPUT(id="mode", name="mode", type="radio", value="1")
    radio2.label = tf.label("Use custom billing details")
    mode.add(radio2)
    radio3 = tf.DIV(id="radio_field3")
    radio3.value = tf.INPUT(id="mode", name="mode", type="radio", value="2")
    radio3.label = tf.label("Another Member")
    mode.add(radio3)
    radio4 = tf.DIV(id="radio_field4")
    radio4.value = tf.INPUT(id="mode", name="mode", type="radio", value="3")
    radio4.label = tf.label("Organization")
    mode.add(radio4)

    details = billing_pref_form.add(sphc.more.Fieldset(id="billing_details"))
    details.add(tf.LEGEND("Billing Details"))
    
    custom = tf.DIV(id="details_1", Class="hidden")
    custom_form = sphc.more.Form(id="custom_details-form", Class='hform')
    custom_form.add_field('Name', tf.INPUT(type='text', id='custom_name', name='custom_name'))
    custom_form.add_field('Address', tf.TEXTAREA(id='custom_address', name='custom_address'))
    custom_form.add_field('City', tf.INPUT(id='custom_city', name='custom_city', type="text"))
    custom_form.add_field('Country', tf.SELECT(fe.src.common.country_options, id='custom_country', name='custom_country'))
    custom_form.add_field('Phone', tf.INPUT(type='text', id='custom_phone', name='custom_phone'))
    custom_form.add_field('Email', tf.INPUT(type='email', id='custom_email', name='custom_email'))
    custom.form = custom_form.build()
    details.add(custom)
    
    member = tf.DIV(id="details_2", Class="hidden")
    member.label = tf.LABEL("Bill To Existing Member")
    member.value = tf.INPUT(id="member", type="text")
    details.add(member)
    
    organization = tf.DIV(id="details_3", Class="hidden")
    organization.radio1 = tf.DIV(id="organization_radio_field1")
    organization.radio1.value = tf.INPUT(id="organization_mode0", name="organization_mode", type="radio", value="0")
    organization.radio1.label = tf.label("Bill To Existing")
    organization.radio1.input = tf.INPUT(type="text", id="existing_org")
    organization.radio2 = tf.DIV(id="organization_radio_field2")
    organization.radio2.value = tf.INPUT(id="organization_mode1", name="organization_mode", type="radio", value="1")
    organization.radio2.label = tf.label("Add New Organization")
    
    organization_form = sphc.more.Form(id="new_org-form")
    organization_form.add_field('Organization Name', tf.INPUT(type='text', id='org_name', name='org_name'))
    organization_form.add_field('Address', tf.TEXTAREA(id='org_address', name='org_address'))
    organization_form.add_field('City', tf.INPUT(id='org_city', name='org_city', type="text"))
    organization_form.add_field('Country', tf.SELECT(fe.src.common.country_options, id='org_country', name='org_country'))
    organization_form.add_field('Phone', tf.INPUT(type='text', id='org_phone', name='org_phone'))
    organization_form.add_field('Email', tf.INPUT(type='email', id='org_email', name='org_email'))
    organization.form = organization_form.build()
    details.add(organization)

    billing_pref_form.add_buttons(tf.INPUT(id="update-billingpref", type="button", value="Update"))

    return billing_pref_form.build()

def add_tariffs_section(container):
    tariff_box = tf.DIV()

    new = tf.DIV(Class="right-action")
    new.button = tf.BUTTON("New", id="next_tariff-btn", name="next_tarrif-btn", type="button")

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
    cell.a = tf.A("Change", href="#/${member_id}/memberships", Class="change-sub", id="change_sub-${id}")
    cell.c = tf.C(" | ")
    cell.a = tf.A('X', title="Cancel tariff", href="#/${member_id}/memberships", Class="cancel-sub", id="cancel_sub-${id}")    
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
    next_tariff_form.add_field("", tf.INPUT(id='end', type="hidden"))
    next_tariff_form.add_field("Stop", tf.INPUT(name='end-vis', id='end-vis'))
    next_tariff_form.add_buttons(tf.BUTTON("Save", id="tariff_save-btn", type="submit"), tf.BUTTON("Cancel", id='tariff_cancel-btn', type="button"))
    next_tariff_section = tf.DIV(id='next-tariff-section', Class='hidden')
    next_tariff_section.form = next_tariff_form.build()
    next_tariff_section.tmpl = tariff_list_row
    container.next_tarrif = next_tariff_section
    
    change_tariff_form = sphc.more.Form(id='change-tariff-form', classes=['vform'])
    change_tariff_form.add_field("", tf.INPUT(type="hidden", id='starts'))
    change_tariff_form.add_field("Start", tf.INPUT(name='starts-vis', id='starts-vis'))
    change_tariff_form.add_field("", tf.INPUT(type="hidden", id='ends'))
    change_tariff_form.add_field("Stop", tf.INPUT(name='ends-vis', id='ends-vis'))
    change_tariff_form.add_buttons(tf.INPUT(value="Save", id="save-btn" ,type="button"), tf.INPUT(value="Cancel", id='cancel-btn' ,type="button"))
    change_tariff_section = tf.DIV(id='change-tariff-section', Class='hidden')
    change_tariff_section.form = change_tariff_form.build()
    change_tariff_section.tmpl = tariff_list_row
    container.change_tarrif = change_tariff_section
    
    #stop_membership_form = sphc.more.Form(id='stop_membership', classes=['hform'])
    #stop_membership_form.add_field("End Date", tf.INPUT(id="stop_date", type="text").set_required())
    #stop_membership_form.add_field("", tf.INPUT(type="hidden", id='stops'))
    #stop_membership_form.add_buttons(tf.INPUT(id="stop-btn", value="Stop", type="submit"))
    #container.stop_membership = stop_membership_form.build()
    
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
    script = "fe/src/js/member_create.js"

    def content(self):
        container = tf.DIV()

        form  = sphc.more.Form(Class='hform simple-hform', id="createmember_form", method="POST")

        sections = []

        section = sphc.more.Fieldset()
        section.add(tf.LEGEND("About"))
        section.add_field('First Name',tf.INPUT(type='text', id='first_name', name='first_name').set_required())
        section.add_field('Last Name', tf.INPUT(type='text', id='last_name', name='last_name'))
        section.add_field('Username', tf.INPUT(type='text', id='username', name='username').set_required())
        section.add_field('Password',tf.INPUT(type='password', id='password', name='password').set_required())
        lang_options = [tf.OPTION(language['label'], value=language['name']) for language in data_lists.languages]
        section.add_field('Language', tf.SELECT(lang_options, id='language', name='language'))
        sections.append(section)

        section = sphc.more.Fieldset()
        section.add(tf.LEGEND("Contact"))
        section.add_field("Address", tf.TEXTAREA(name='address', type="text"))
        section.add_field("City", tf.INPUT(name='city', type="text"))
        section.add_field("Country", tf.SELECT(fe.src.common.country_options, id='country', name='country'))
        section.add_field("Zipcode", tf.INPUT(name='pincode', type="text"))
        section.add_field("Phone", tf.INPUT(name='phone', type="text"))
        section.add_field("Mobile", tf.INPUT(name='mobile', type="text"))
        section.add_field("Fax", tf.INPUT(name='mobile', type="text"))
        section.add_field("Email", tf.INPUT(name='email', type="email").set_required())
        section.add_field("Skype", tf.INPUT(name='skype', type="text"))
        sections.append(section)

        for section in sections:
            form.add(section.build())
        form.add_buttons(tf.BUTTON("Create", id='save-btn', type='submit'))

        container.form = form.build()

        return container

    def sidebar(self):
        #content = tf.DIV(tf.DIV("Related", Class="title"))
        content = tf.DIV()
        content.invite = tf.DIV(id='invite', Class='hidden')
        content.invite.form = fe.src.forms.signup_form().build()
        content.help = tf.DIV("You may choose invite Hub hosts to join. It is safer and quicker option.")
        content.action = tf.BUTTON("Invite", href="", Class="bigger-button", id="invite-btn")
        return content

class EditProfile(BasePage):
    current_nav = 'Members'
    title = ''
    content_title = ''

    def content(self):
        container = tf.DIV()

        # Info
        info = tf.DIV(id="info", Class="labeled-list hidden")
        info.id = tf.DIV([tf.DIV("Membership id", Class="label"), tf.C(Class="data-id")], Class="individual")
        info.id = tf.DIV([tf.DIV("Organization id", Class="label"), tf.C(Class="data-id")], Class="organization")
        info.username = tf.DIV([tf.DIV("Username", Class="label"), tf.C(Class="data-username")], Class="individual")
        info.membership = tf.DIV([tf.DIV("Membership", Class="label"), tf.C(Class="data-membership")], Class="individual")
        info.email = tf.DIV([tf.DIV("Email", Class="label"), tf.A(href="", Class="data-email-link")])
        info.line = tf.hr(Class="light")
        
        # Profile
        profile = tf.DIV(id="profile")

        # About
        about_form = sphc.more.Form(id='about', Class='profile-edit-form', classes=['hform'])
        about = about_form.add(sphc.more.Fieldset())
        about.add(tf.LEGEND("About"))
        about.add_field("First Name", tf.INPUT(name='first_name', type="text").set_required(), container_classes=['individual'])
        about.add_field("Last Name", tf.INPUT(name='last_name', type="text"), container_classes=['individual'])
        about.add_field("Name", tf.INPUT(name='name', type="text"), container_classes=['organization'])
        about.add_field("Short description", tf.INPUT(name='short_description', type="text"))
        about.add_field("Long description", tf.TEXTAREA(name='long_description', type="text"))
        about.add_buttons(tf.BUTTON("Update", type="submit"))
        profile.about = about_form.build()

        # Account
        profile.account = tf.FIELDSET(Class="individual")
        profile.account.legend = tf.LEGEND("Account")
        profile.account.account_div = tf.DIV(id="account")
        profile.account.account_div.form = account_form().build()
                
        # Contact
        profile.contact = tf.FIELDSET()
        profile.contact.legend = tf.LEGEND("Contact")
        profile.contact.contact_div = tf.DIV(id="contact")
        profile.contact.contact_div.form = contact_form().build()

        # Preferences
        profile.preferences = tf.FIELDSET(Class="individual")
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
        usages.new = tf.DIV(tf.Button("New", type="button", id="new_usage-btn"))
        add_usage_form = sphc.more.Form(id='add-usage-form', action='#', Class='profile-edit-form', classes=['hform'])
        add_usage = add_usage_form.add(sphc.more.Fieldset(id="add_usage", Class="hidden"))
        add_usage.add(tf.LEGEND("Add Usage"))
        add_usage.add_field("Resource Name", tf.SELECT(id="resource_select", name="resource_select"), tf.INPUT(name='resource_name', id='resource_name', Class="field-input", placeholder="Resource name").set_required())
        add_usage.add_field("Quantity", tf.INPUT(name='quantity', id='quantity', placeholder="eg. 10. Not applicable for time based resource"), fhelp="For non time based resources. Do not include unit")
        add_usage.add_field("Start", tf.INPUT(name='start_time', id='start_time', nv_attrs=('required',)))
        add_usage.add_field("End", tf.INPUT(name='end_time', id='end_time'), "Optional. Only for time based resources.")
        add_usage.add_field("Cost", tf.INPUT(name='cost', id='cost'))
        add_usage.add_buttons(tf.INPUT(id="calculate_cost-btn", type="Button", value="Calculate Cost", Class="big-button"), '→', tf.INPUT(type="button", value="Add", id='submit-usage', Class="big-button", disabled="disabled"), tf.INPUT(type="button", value="Cancel", Class="big-button cancel-usage"))
        usages.add_usage = add_usage_form.build()

        edit_usage = tf.FIELDSET(id="edit_usage", Class="hidden")
        edit_usage.legend = tf.LEGEND("Edit Usage")
        edit_usage_form = sphc.more.Form(id='edit_usage-form', action='#', Class='profile-edit-form', classes=['hform'])
        edit_usage_form.add_field("Resource Name", tf.SELECT(id="res_select", name="res_select"), tf.INPUT(name='res_name', id='res_name', Class="field-input",  placeholder="Resource name").set_required())
        edit_usage_form.add_field("Quantity", tf.INPUT(name='res_quantity', id='res_quantity', placeholder="eg. 10. Not applicable for time based resource"), fhelp="For non time based resources. Do not include unit")
        edit_usage_form.add_field("Start", tf.INPUT(name='res_start_time', id='res_start_time', nv_attrs=('required',)))
        edit_usage_form.add_field("End", tf.INPUT(name='res_end_time', id='res_end_time'), "Optional. Only for time based resources.")
        edit_usage_form.add_field("Cost", tf.INPUT(name='res_cost', id='res_cost'))
        edit_usage_form.add_buttons(tf.INPUT(id="recalculate_cost-btn", type="Button", value="Recalculate Cost", Class="big-button"), '→', tf.INPUT(type="button", value="Save", id='update-usage', Class="big-button"), tf.INPUT(type="button", value="Cancel", Class="big-button cancel-usage"))
        edit_usage.form = edit_usage_form.build()
        usages.edit_usage = edit_usage

        usages.resource_select_tmpl = sphc.more.jq_tmpl("resource-tmpl")
        usages.resource_select_tmpl.option = tf.OPTION("${name}", id="resource_${id}", value="${id}")

        uninvoiced = tf.FIELDSET(id="uninvoiced_usages")
        uninvoiced.legend = tf.LEGEND("Uninvoiced Usages")
        uninvoiced.table = tf.TABLE(id="usage_table")
        usages.uninvoiced = uninvoiced

        #Invoices
        invoices = tf.DIV(id="invoices")
        invoice_summary = tf.DIV(id="invoice_summary")
        invoice_summary.new_invoice = tf.DIV(tf.Button("New", type="button", id="new_invoice-btn"))
        invoice_history = tf.FIELDSET()
        invoice_history.legend = tf.LEGEND("Invoice History")
        invoice_history.table = tf.TABLE(id="history_table")
        invoice_history.view_invoice_dialog = tf.DIV(id="view_invoice_window", Class='hidden')
        invoice_history.view_invoice_dialog.frame = tf.IFRAME(id="invoice-iframe", src="#", width="800", height="600")
        invoices.invoice_summary = invoice_summary
        invoices.table = invoice_history

        # Profile Tabs
        container.tabs = tf.DIV(id="profile_tabs")
        container.tabs.list = tf.UL()
        container.tabs.list.tab1 = tf.li(tf.A("Info", href="#info", Class="profile-tab"))
        container.tabs.list.tab1 = tf.li(tf.A("Profile", href="#profile", Class="profile-tab"))
        container.tabs.list.tab2 = tf.li(tf.A("Memberships", href="#memberships", Class="profile-tab"))
        container.tabs.list.tab3 = tf.li(tf.A("Billing Preferences", href="#billing", Class="profile-tab individual"), CLass="individual")
        container.tabs.list.tab4 = tf.li(tf.A("Usages", href="#usages", Class="profile-tab"))
        container.tabs.list.tab5 = tf.li(tf.A("Invoices", href="#invoices", Class="profile-tab"))
        container.tabs.info = info
        container.tabs.profile = profile
        container.tabs.memberships = memberships
        container.tabs.billing = billing
        container.tabs.usages = usages
        container.tabs.invoices = invoices

        container.script = sphc.more.script_fromfile("fe/src/js/member_edit.js")
        
        return container

