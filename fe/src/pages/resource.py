# -*- coding: UTF-8 -*-

import sphc
import sphc.more
import fe.bases
import commonlib.shared.static as static

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

class ResourceCreate(BasePage):
    current_nav = 'Resources'
    title = 'New Resource'
    def content(self):
        container = tf.DIV()

        form = sphc.more.Form(id='createresource_form', classes=['hform'], enctype='multipart/form-data')
        form.add_field('Name', tf.INPUT(type='text', id='name', name='name').set_required())
        resource_types = tf.SELECT(id='type', name='type')
        for rtype in static.resource_types:
            resource_types.option = tf.OPTION(rtype['label'], value = rtype['name'])
        form.add_field('Type', resource_types)
        time_based = tf.SPAN()
        time_based.input = tf.INPUT(type='checkbox', id='calc_mode', name='calc_mode')
        time_based.label = tf.LABEL('Time Based', FOR="time_based")
        form.add_field("", time_based)
        form.add_field('Default Price', tf.INPUT(type="text", name='default_price').set_required(), fhelp="Will be added to Guest Tariff. Used in calculating cost of a usage by a person without a membership")
        form.add_field('Picture', tf.INPUT(name="picture", id="picture", type="file", accept="image/*"), "Suggested Image Dimensions : 250x250.")
        form.add_field('Short Description', tf.TEXTAREA( id='short_description', name='short_description'))
        form.add_field('Long Description', tf.TEXTAREA(id='long_description', name='long_description'))
        form.add_field('Accounting Code', tf.INPUT(type='text', id='accnt_code', name='accnt_code'))
        form.add_buttons(tf.BUTTON("Save", type='submit'))
        container.form = form.build()
        container.script = sphc.more.script_fromfile("fe/src/js/resource_create.js")
        return container

class ResourceManage(BasePage):
    current_nav = 'Resources'
    title = 'Manage resources'
    content_menu = [tf.A('+ Create New', href="/${lang}/${theme}/resource/new", Class="item")]
    def content(self):
        container = tf.DIV()

        types = tf.DIV("Types : ", id="resource_types", Class="resource_types")
        for rtype in static.resource_types:
            types.type = tf.INPUT(value=rtype['label'], type="Button", Class="resource_type-hide", id="rtype_"+rtype['name'])

        filters = tf.DIV("Filters : ", id="resource_filters", Class="resource_filters")
        filters.attr1 = tf.INPUT(value="Enabled", type="Button", Class="resource_filter-hide", id="enabled")
        filters.attr2 = tf.INPUT(value="Host Only", type="Button", Class="resource_filter-hide", id="host_only")
        filters.attr3 = tf.INPUT(value="Repairs", type="Button", Class="resource_filter-hide", id="repairs")

        resource_list = tf.DIV(Class='list-boxes', id="resource_list")
        resource_tmpl = sphc.more.jq_tmpl("resource-tmpl")
        resource_tmpl.box = tf.DIV(Class='row resource-hidden filtered_resource-visible typed_resource-hidden', id="resource_${id}")
        resource_tmpl.box.second = tf.DIV(Class='resource-data_part')
        resource_tmpl.box.second.name = tf.DIV()
        resource_tmpl.box.second.name.link = tf.A("${name}", id="edit_${id}", href="#/${id}/edit/profile", Class="row-title")
        resource_tmpl.box.second.description = tf.DIV("${short_description}", id="short_description_${id}")
        resource_tmpl.box.third = tf.DIV(Class='resource-filter_part')
        resource_tmpl.box.third.clock = tf.C("◴", title="Time Based", id="clock_${id}", Class="text-xl", escape="false")

        resource_edit_form = sphc.more.Form(id='resource_edit_form', classes=['hform'])
        resource_edit_form.add_field("Name", tf.INPUT(id="name", type="text"))
        resource_type_list = tf.SELECT(id="type")
        for rtype in static.resource_types:
            resource_type_list.option = tf.OPTION(rtype['label'], value = rtype['name'])
        resource_edit_form.add_field("Type", resource_type_list)
        time_based = tf.DIV()
        time_based.field = tf.INPUT(id="time_based", type="checkbox")
        time_based.label = tf.C("Time Based")
        resource_edit_form.add_field("", time_based)
        resource_edit_form.add_field("Picture", tf.INPUT(id="picture", type="file"), "Suggested Image Dimensions : 250x250.")
        resource_edit_form.add_field("Short Description", tf.TEXTAREA(id="short_desc"))
        resource_edit_form.add_field("Long Description", tf.TEXTAREA(id="long_desc"))
        resource_edit_form.add_field('Accounting Code', tf.INPUT(type='text', id='accnt_code', name='accnt_code'))
        resource_states = tf.DIV()
        resource_states.state1 = tf.INPUT(id="state_enabled", type="checkbox")
        resource_states.label1 = tf.C("Enabled")
        resource_states.state2 = tf.INPUT(id="state_host_only", type="checkbox")
        resource_states.label2 = tf.C("Host Only")
        resource_states.state3 = tf.INPUT(id="state_repairs", type="checkbox")
        resource_states.label3 = tf.C("Repairs")
        resource_edit_form.add_field("", resource_states)
        resource_edit_form.add_buttons(tf.INPUT(type="button", value="Update", id='update_resource-btn'), tf.INPUT(type="button", value="Cancel", id='cancel-btn'))
        #resource_edit = tf.DIV(id="resource_edit")
        #resource_edit.form = resource_edit_form.build()

        # Tabs
        tab_container = tf.DIV(Class="tab-container hidden")
        tab_container.tabs = tf.DIV(id="tabs", Class="tabs")
        tab_container.tabs.items = [tf.A(tf.DIV("Profile"), href="#/ID/edit/profile", id="res-profile-tab", Class="tab"),
            tf.A(tf.DIV("Pricing"), href="#/ID/edit/pricing", id="res-pricing-tab", Class="tab"),
            tf.A(tf.DIV("Taxes"), href="#/ID/edit/taxes", id="res-taxes-tab", Class="tab")]
        tab_container.profile = tf.DIV(resource_edit_form.build(), id="res-profile-content", Class="tab-content")

        pricing = tf.DIV(id="res-pricing-content", Class="tab-content")

        pricing.price_tmpl = sphc.more.jq_tmpl("price-tmpl")
        pricing.price_tmpl.col = tf.DIV([tf.DIV("${tariff_name}", Class="text-small"), tf.DIV("${amount}", Class="text-xl")], Class="cell")
        pricing.current = tf.DIV(id="current-prices")
        pricing.hr = tf.HR()

        pricing.tariff_option = sphc.more.jq_tmpl("tariff-option-tmpl")
        pricing.tariff_option.li = tf.OPTION("${name}", value="${id}", name="tariff")

        pricing.tariff_dropdown = tf.DIV(tf.SELECT(tf.OPTION("Select tariff", selected="true", disabled="true"), id="tariff-select").set_required())
        #pricing.tip = tf.DIV(tf.C("Schedule new price"))
        pricing.pricing_tmpl = sphc.more.jq_tmpl("old-pricing-tmpl")
        pricing.pricing_tmpl.pricing = tf.DIV(Class="pricing")
        view_pricing = tf.DIV(id="pricing-${id}")
        view_pricing.starts = tf.SPAN("${starts}", Class="pricing-date", id="pricing_date-${id}")
        view_pricing.amount = tf.SPAN("${amount}", Class="pricing-amt", id="pricing_amount-${id}")
        view_pricing.edit = tf.SPAN(tf.A("Edit", id="pedit-${id}", Class="pricing_edit-link"))
        view_pricing.cancel = tf.SPAN(tf.A("X", id="pricing_${id}", Class="cancel-x"))
        edit_pricing = tf.FORM(id="edit_pricing-${id}", Class="edit-pricing hidden", method="POST")
        edit_pricing.start_vis = tf.SPAN(tf.INPUT(placeholder="From date", type="text", id='edit_starts_vis-${id}').set_required())
        edit_pricing.starts = tf.INPUT(id='edit_starts-${id}', type="hidden", value="-")
        edit_pricing.amount = tf.SPAN(tf.INPUT(type="text", id='edit_amount-${id}', value="${amount}").set_required())
        edit_pricing.save = tf.SPAN(tf.BUTTON("Save", type="submit"))
        edit_pricing.cancel = tf.SPAN(tf.BUTTON("Cancel", type="button", Class="edit-cancel", id="cancel_edit-${id}"))
        pricing.pricing_tmpl.pricing.view = view_pricing
        pricing.pricing_tmpl.pricing.edit = edit_pricing

        pricing.new = tf.FORM(id="new-pricing", method="POST", Class="hidden")
        pricing.new.starts_vis = tf.SPAN(tf.INPUT(placeholder="From date", type="text", id='new-starts-vis'))
        pricing.new.starts = tf.INPUT(id='new-starts', type="hidden").set_required()
        pricing.new.amount = tf.SPAN(tf.INPUT(placeholder="New price", type="text", id='new-amount').set_required())
        pricing.new.action = tf.SPAN(tf.BUTTON("Add", type="submit"))

        pricing.table = tf.DIV(id="old-pricings", Class="grid")

        taxation = tf.DIV(id="res-taxes-content", Class="tab-content")
        taxes = sphc.more.Form(id="taxation", Class="hform")
        taxes.add(tf.DIV([tf.INPUT(id="tax_mode0", type="radio", name="tax_mode", value="0"), tf.label("Use %s level taxes" % __("coworking place"))]))
        taxes.add(tf.DIV([tf.INPUT(id="tax_mode1", type="radio", name="tax_mode", value="1"), tf.label("Use following taxes")]))
        add_tax = tf.DIV(id="add_tax")
        add_tax.name = tf.DIV(tf.INPUT(placeholder="Tax name", type="text", id='new_tax'), Class='tax-name')
        add_tax.value = tf.DIV([tf.INPUT(placeholder="Value: eg. 10 for 10%", type="number", id='new_value', step="0.1"), tf.span("%")], Class='tax-value')
        add_tax.action = tf.DIV(tf.BUTTON("Add", type="button", id="add_tax-btn"), Class="tax-delete")
        taxes.add_field("", tf.DIV(add_tax, id="taxes_list"))
        taxes.add_buttons(tf.BUTTON("Save", id="save-btn", type="submit"))
        tax_template = sphc.more.jq_tmpl('tax_tmpl')
        tax_template.new_tax = tf.DIV(Class="new-tax")
        tax_template.new_tax.name = tf.DIV(tf.INPUT(type="text", value="${name}", Class="new-name").set_required(), Class='tax-name')
        tax_template.new_tax.value = tf.DIV([tf.INPUT(type="number", value="${value}", Class="new-value", step="0.1").set_required(), tf.span("%")], Class='tax-value')
        tax_template.new_tax.delete = tf.DIV(tf.A("X", href="#"), Class="tax-delete remove-tax")

        taxation.taxes = taxes.build()
        taxation.template = tax_template
        
        container.list_container = tf.DIV(id="list-container", Class="hidden")
        container.list_container.types = types
        container.list_container.filters = filters
        container.list_container.resource_tmpl = resource_tmpl
        container.list_container.resource_list = resource_list
        container.resource_tabs = tab_container
        container.resource_tabs.pricing = pricing
        container.resource_tabs.taxation = taxation

        container.script = sphc.more.script_fromfile("fe/src/js/resource_manage.js")
        return container
