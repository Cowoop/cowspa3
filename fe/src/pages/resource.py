# -*- coding: UTF-8 -*-

import sphc
import sphc.more
import fe.bases
import commonlib.shared.static as static

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

class ResourceCreate(BasePage):
    current_tab = 'Resources'
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
        time_based.input = tf.INPUT(type='checkbox', id='time_based', name='time_based')
        time_based.label = tf.LABEL('Time Based', FOR="time_based")
        form.add_field("", time_based)
        form.add_field('Picture', tf.INPUT(name="picture", id="picture", type="file", accept="image/*"), "Suggested Image Dimensions : 250x250.")
        form.add_field('Short Description', tf.TEXTAREA( id='short_description', name='short_description'))
        form.add_field('Long Description', tf.TEXTAREA(id='long_description', name='long_description'))
        form.add_buttons(tf.BUTTON("Save", type='submit'))
        container.form = form.build()
        container.script = sphc.more.script_fromfile("fe/src/js/resource_create.js")
        return container

class ResourceManage(BasePage):
    current_tab = 'Resources'
    title = 'Manage resources'
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
        tab_container = tf.DIV(id="resource_tabs", Class="hidden")
        tab_container.tabs = tf.UL([tf.LI(tf.A("Profile", href="#resource_profile")), tf.LI(tf.A("Pricing", href="#resource_pricing"))])
        tab_container.profile = tf.DIV(id="resource_profile")
        tab_container.profile.content = resource_edit_form.build()
        tab_container.pricing = tf.DIV(id="resource_pricing")

        tab_container.pricing.content = tf.C("123")

        container.types = types
        container.filters = filters
        container.resource_tmpl = resource_tmpl
        container.resource_list = resource_list
        container.resource_tabs = tab_container

        container.script = sphc.more.script_fromfile("fe/src/js/resource_manage.js")
        return container
