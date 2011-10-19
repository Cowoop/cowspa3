# -*- coding: UTF-8 -*-

import sphc
import fe.bases
import commonlib.shared.static as static

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

class ResourceCreate(BasePage):
    current_tab = 'create'
    title = 'New Resource'
    def content(self):
        container = tf.DIV()

        fields = []

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Name : ', For='name')
        field.input = tf.INPUT(type='text', id='name', name='name')
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL('Type : ', FOR='type')
        field.input = tf.SELECT(id='type', name='type')
        for rtype in static.resource_types:
            field.input.option = tf.OPTION(rtype['label'], value = rtype['name'])
        fields.append(field)
        
        field = tf.DIV()
        field.label = tf.LABEL(content = 'Picture : ', FOR="picture")
        field.input = tf.INPUT(name="picture", id="picture", type="file", accept="image/*")
        fields.append(field)
    
        field = tf.DIV()
        field.label = tf.LABEL(content = 'Short Description : ', FOR="short_description")
        field.input = tf.TEXTAREA( id='short_description', name='short_description', rows=2, cols=25)
        fields.append(field)

        field = tf.DIV()
        field.label = tf.LABEL(content = 'Long Description : ', FOR="long_description")
        field.input = tf.TEXTAREA(id='long_description', name='long_description', rows=5, cols=25)
        fields.append(field)

        field = tf.DIV()
        field.input = tf.INPUT(type='checkbox', id='time_based', name='time_based')
        field.text = 'Time Based'
        fields.append(field)
        
        field = tf.DIV()
        field.button = tf.BUTTON("Save", id='save-btn', type='button')
        fields.append(field)

        form  = tf.FORM(Class='profile-forms', id="createresource_form")
        for field in fields:
            field.line = tf.BR()
            form.content = field
    
        container.form = form
        container.msg = tf.SPAN(id="CreateResource-msg")
        container.script = tf.SCRIPT(open("fe/src/js/resource_create.js").read(), escape=False, type="text/javascript", language="javascript")
        return container
        
class ResourceManage(BasePage):
    current_tab = 'manage'
    title = 'Manage Resources'
    def content(self):
        container = tf.DIV()
        
        types = tf.DIV("Types : ", id="resource_types", Class="resource_types")
        for rtype in static.resource_types:
            types.type = tf.INPUT(value=rtype['label'], type="Button", Class="resource_type-hide")
        
        filters = tf.DIV("Filters : ", id="resource_filters", Class="resource_filters")
        filters.attr1 = tf.INPUT(value="Enabled", type="Button", Class="resource_filter-hide", id="enabled")
        filters.attr2 = tf.INPUT(value="Host Only", type="Button", Class="resource_filter-hide", id="host_only")
        filters.attr3 = tf.INPUT(value="Repairs", type="Button", Class="resource_filter-hide", id="repairs")
        
        resource_list = tf.DIV(Class='resource-list', id="resource_list")
        resource_tmpl = sphc.more.jq_tmpl("resource-tmpl")
        resource_tmpl.box = tf.DIV(Class='resource-box resource-hidden filtered_resource-visible typed_resource-hidden', id="resource_${id}")
        resource_tmpl.box.first = tf.DIV(Class='resource-image_part')
        resource_tmpl.box.first.picture = tf.IMG(Class='resource_list-logo', src="${picture}", id="picture_${id}")
        resource_tmpl.box.second = tf.DIV(Class='resource-data_part')
        resource_tmpl.box.second.name = tf.DIV()
        resource_tmpl.box.second.name.link = tf.A("${name}", id="${id}", href="#")
        resource_tmpl.box.second.description = tf.DIV("${short_description}", id="short_description_${id}")
        resource_tmpl.box.third = tf.DIV(Class='resource-filter_part')
        resource_tmpl.box.third.clock = tf.H2("◴", title="Time Based", id="clock_${id}")
        
        container.types = types
        container.filters = filters
        container.resource_tmpl = resource_tmpl
        container.resource_list = resource_list
        
        container.script = tf.SCRIPT(open("fe/src/js/resource_manage.js").read(), escape=False, type="text/javascript", language="javascript")     
        return container
