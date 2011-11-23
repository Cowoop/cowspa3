import sphc
import fe.bases
import commonlib.shared.static as data_lists

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

def get_location_form():
    form = sphc.more.Form(id='bizplace_form', classes=['hform'])
    about = form.add(sphc.more.Fieldset())
    about.add(sphc.tf.LEGEND('About'))
    about.add_field('Name', sphc.tf.INPUT(name='name', type='text'))
    about.add_field('Address', sphc.tf.TEXTAREA(id='address', name='address'))
    about.add_field('City', sphc.tf.INPUT(type='text', id='city', name='city'))
    country_select = sphc.tf.SELECT(id='country', name='country')
    country_select.options = fe.src.common.country_options
    about.add_field('Country', country_select)

    #tz_select = sphc.tf.SELECT(id='tz', name='tz')
    #tz_select.options = fe.src.common.tz_options
    #about.add_field('Time zone', tz_select)

    about.add_field('Short Description', sphc.tf.TEXTAREA(id='short_description',
            name='short_description', rows=2, cols=25))
    curr_select = sphc.tf.SELECT(id='currency', name='currency')
    for currency in data_lists.currencies:
        curr_select.option = sphc.tf.OPTION(currency['label']+" ("+currency['name']+")", 
                        value=currency['name'])
    about.add_field('Currency', curr_select)

    contact = form.add(sphc.more.Fieldset())
    contact.add(sphc.tf.LEGEND('Contact Details'))

    contact.add_field('Phone', sphc.tf.INPUT(id='phone', name='phone'))
    contact.add_field('Fax', sphc.tf.INPUT(id='fax', name='fax'))
    contact.add_field('Email', sphc.tf.INPUT(type='email', id='email',
        name='email').set_required())
    contact.add_field('Booking Email', sphc.tf.INPUT(type='email', id='booking_email',
            name='booking_email'))
    contact.add_field('Host Email', sphc.tf.INPUT(type='email', id='host_email',
        name='host_email'))

    return form

class Create(BasePage):
    current_nav = 'Locations'
    title = 'New Location'

    def content(self):
        container = tf.DIV()
        form = get_location_form()
        form.add_buttons(tf.BUTTON("Create", id='save-btn', type="submit"))
        container.form = form.build()
        container.script = sphc.more.script_fromfile("fe/src/js/bizplace_create.js")
        return container

class List(BasePage):

    title = "Locations"
    current_nav = 'Locations'

    def content(self):
        container = tf.DIV()

        my_locations = tf.DIV(id='my-locations', Class='location-list')
        all_locations = tf.DIV(id='all-locations', Class='location-list')

        # Tabs
        container.tabs = tf.DIV(id="location_tabs")
        container.tabs.list = tf.UL()
        container.tabs.list.tab1 = tf.li(tf.A("My Locations",
            href="#my-locations"))
        container.tabs.list.tab2 = tf.li(tf.A("All Locations",
            href="#all-locations"))

        # My Locations
        my_loc_list = tf.DIV(id='my_loc_list')
        my_loc_tmpl = sphc.more.jq_tmpl('my_loc_tmpl')
        my_loc_tmpl.box = tf.DIV(Class='location-box')
        my_loc_tmpl.box.info = tf.DIV(Class='loc_info_part')
        my_loc_tmpl.box.info.link = tf.A("${label}", id='edit-link_${id}', 
                href='#/${id}', Class='location-title')
        my_loc_tmpl.box.info.my_role = tf.DIV(Class='location-description')
        my_loc_tmpl.box.info.my_role.label = tf.LABEL("My Role(s) : ")
        my_loc_tmpl.box.info.my_role.role = tf.LABEL("${roles}")

        loc_buttons = tf.DIV(Class="buttons")
        loc_buttons.tariff_btn = tf.BUTTON("Tariff", id='myloc_tariff_btn-${id}',
                Class='myloc_tariff-btn', type='button')
        loc_buttons.team_btn = tf.BUTTON("Team", id='myloc_team_btn-${id}',
                Class='myloc_team-btn', type='button')
        my_loc_tmpl.box.btn = tf.DIV(Class='loc_btns_part')
        my_loc_tmpl.box.btn.buttons = loc_buttons

        my_loc_list.loc_tmpl = my_loc_tmpl

        my_locations.my_loc_list = my_loc_list

        # View Location Details
        edit = tf.DIV(Class="edit-link-box")
        edit.link = tf.A("Edit", id='edit-link', href='')
        fields = [edit]

        cancel = tf.DIV(Class="edit-link-box")
        cancel.link = tf.A("Back to List", id='cancel-link', href='#')
        fields.append(cancel)

        form = get_location_form()
        buttons = tf.DIV(Class="buttons")
        buttons.save = tf.BUTTON("Save", id='save-btn', type='submit')
        buttons.cancel = tf.BUTTON("Cancel", id='cancel-btn', type='button')
        form.add_buttons(buttons)

        my_locations.form = form.build()

        field_data = [('Name', 'name'),
            ('Address', 'address'),
            ('City', 'city'),
            ('Country', 'country'),
            ('Short description', 'short_description'),
            ('Currency', 'currency'),
            ('Phone','phone'),
            ('Fax','fax'),
            ('Email', 'email'),
            ('Host Email', 'host_email'),
            ('Booking Email', 'booking_email')
            ]
        for label, name in field_data:
            field = tf.DIV(Class="field-container")
            field.label = tf.DIV(label, Class="field-name")
            field.value = tf.DIV(id=name, Class="field-value")
            fields.append(field)

        view = tf.DIV(id="location_view_form")
        view.fields= fields

        my_locations.view = view

        # All Locations
        all_loc_list = tf.DIV(id='all_loc_list')
        all_loc_tmpl = sphc.more.jq_tmpl('all_loc_tmpl')
        all_loc_tmpl.box = tf.DIV(Class='location-box')
        all_loc_tmpl.box.info = tf.DIV(Class='loc_info_part')
        all_loc_tmpl.box.info.link = tf.A("${name}", id='edit-link_${id}', 
                href='#/${id}', Class='location-title')
        all_loc_tmpl.box.info.city = tf.LABEL("${city}, ${country}", 
                Class='location-info')
        all_loc_tmpl.box.info.short_description = tf.DIV("${short_description}", 
                Class='location-description')

        all_buttons = tf.DIV(Class="buttons")
        all_buttons.tariff_btn = tf.BUTTON("Tariff", id='allloc_tariff_btn-${id}',
                Class='myloc_tariff-btn', type='button')
        all_loc_tmpl.box.btn = tf.DIV(Class='loc_btns_part')
        all_loc_tmpl.box.btn.buttons = all_buttons

        all_loc_list.loc_tmpl = all_loc_tmpl
        all_locations.all_loc_list = all_loc_list


        # View Location Details
        cancel = tf.DIV(Class="edit-link-box")
        cancel.link = tf.A("Back to List", id='cancel-link', href='#')
        fields = [cancel]

        for label, name in field_data:
            field = tf.DIV(Class="field-container")
            field.label = tf.DIV(label, Class="field-name")
            field.value = tf.DIV(id=name, Class="field-value")
            fields.append(field)

        all_loc_view = tf.DIV(id="all_location_view")
        all_loc_view.fields= fields

        all_locations.view = all_loc_view

        container.tabs.myloc = my_locations
        container.tabs.all_loc = all_locations

        container.script = sphc.more.script_fromfile("fe/src/js/list_locations.js")

        return container

