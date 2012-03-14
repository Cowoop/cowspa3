//***************************** Global Section ***********************************
var picture = null;
var resource_list = {};
var state = 0;
var checked_map = {'checked':true, 'on':true, undefined:false};
var time_based_map = {'checked':1, 'on':1, undefined:0};
var calc_map = {'time_based':1, 'quantity_based':0};
var image_size_limit = 256000;//256kb
var res_id = null;
var this_resource = null;
var this_res_pricing = null;
var this_res_taxes = null;
//xxxxxxxxxxxxxxxxxxxxxxxxxxx End Global Section xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

// Routing

function setup_routing () {
    var routes = {
        '/:id': {
            '/edit/profile' : get_resource,
            '/edit/pricing' : get_pricing,
            '/edit/taxes' : get_taxes,
            on: act_on_route
        },
    };
    Router(routes).configure({ recurse: 'forward' }).init();
};

function act_on_route(id) {
    res_id = id;
    this_resource_id = id;
    view_resource_tabs();
    $('.tab').each( function () {
        var href = $(this).attr('href');
        var new_href = href.replace('ID', id);
        $(this).attr('href', new_href);
    });
    $('.tab[href="'+window.location.hash+'"]').addClass('tab-selected');
};

// Tabs

$('.tab').click( function () {
    $('.tab').removeClass('tab-selected');
    $(this).addClass('tab-selected');
});


function view_resource_tabs() {
    $('.tab-container').show();
    $('#list-container').hide();
    $('.tab-content').hide();
};

function view_resource_list() {
    $('.tab-container').hide();
    $('#list-container').show();
    window.location.hash = '';
};

//****************************List Resource*************************************

function on_resource_data(resource) {
    resource_list[resource.id] = resource;
    if(resource.calc == calc_map.quantity_based) {
        $("#clock_"+resource.id).hide();
    };
};

function on_list_resources(resp) {
    var result = resp.result;
    $('#resource-tmpl').tmpl(result).appendTo('#resource_list');
    for (var i=0; i< result.length; i++) {
        on_resource_data(result[i]);
    };
    view_resource_list();
    $("#rtype_room").click();
};

if (window.location.hash == '') {
    function error(){};
    jsonrpc('resource.list', {'owner':current_ctx}, on_list_resources, error);
};

function load_resource(resp) {
    on_resource_data(resp.result);
    resource_editing();
};

function get_resource(id) {
    if ((this_resource == null) || (this_resource.id != id)) {
        function error(resp) {};
        jsonrpc('resource.info', {'res_id':id}, load_resource, error);
    } else { resource_editing(); };
};

//xxxxxxxxxxxxxxxxxxxxxxxxxxxEnd List Resourcexxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

//***************************Upload Resource Picture****************************
$('#picture').change(function handleFileSelect(evt) {
    var files = evt.target.files;
    var reader = new FileReader();
    reader.onload = (function(e) {
        picture = e.target.result;
    });
    if(files.length == 1){
        if(files[0].size <= image_size_limit)
            reader.readAsDataURL(files[0]);
        else
            alert("Image size exceeds image upload limit, Image size must be less than "+ (image_size_limit/1000) + "kb.");
    }
});
//xxxxxxxxxxxxxxxxxxxxxxxxxEnd Upload Invoice Picturexxxxxxxxxxxxxxxxxxxxxxxxxxx

//*****************************On Resource Type Click***************************
function show_resource(){
    $(this).attr('class', 'resource_type-show');
    var type = ($(this).val()).toLowerCase();
    $('.typed_resource-hidden').each(function(){
        res_id = parseInt($(this).attr('id').split('_')[1], 10);
        if(resource_list[res_id]['type'] == type){
            $(this).removeClass("typed_resource-hidden");
            $(this).addClass("typed_resource-visible");
        }
        if($(this).hasClass('typed_resource-visible') && $(this).hasClass('filtered_resource-visible')){
            $(this).removeClass("resource-hidden");
            $(this).addClass("resource-visible");
        }
        else{
            $(this).addClass("resource-hidden");
            $(this).removeClass("resource-visible");
        }
    });
    $('.resource_type-show').click(hide_resource);
};

function hide_resource(){
    $(this).attr('class', 'resource_type-hide');
    type = ($(this).val()).toLowerCase();
    $('.typed_resource-visible').each(function(){
        res_id = parseInt($(this).attr('id').split('_')[1], 10);
        if(resource_list[res_id]['type'] == type){
            $(this).addClass("typed_resource-hidden");
            $(this).removeClass("typed_resource-visible");
            $(this).addClass("resource-hidden");
            $(this).removeClass("resource-visible");
        }
    });
    $('.resource_type-hide').click(show_resource);
};

$('.resource_type-hide').click(show_resource);
$('.resource_type-show').click(hide_resource);
//xxxxxxxxxxxxxxxxxxxxxxxxxxxxEnd On Resource Type Clickxxxxxxxxxxxxxxxxxxxxxxxx

//***************************On Resource Filter Click***************************
function show_filtered_resources(){
    state |= states[$(this).attr('id')];
    $('.filtered_resource-visible').each(function(){
        res_id = parseInt($(this).attr('id').split('_')[1], 10);
        if((resource_list[res_id].flag & state) != state){
            $(this).removeClass("filtered_resource-visible");
            $(this).addClass("filtered_resource-hidden");
            $(this).removeClass("resource-visible");
            $(this).addClass("resource-hidden");
        }
    });
    $(this).unbind('click');
    $(this).attr('class', 'resource_filter-show');
    $(this).click(hide_filtered_resources);
};

function hide_filtered_resources(){
    state ^= states[$(this).attr('id')];
    $('.filtered_resource-hidden').each(function(){
        res_id = parseInt($(this).attr('id').split('_')[1], 10);
        if((resource_list[res_id].flag & state) == state){
            $(this).addClass("filtered_resource-visible");
            $(this).removeClass("filtered_resource-hidden");
        }
        if($(this).hasClass('typed_resource-visible') && $(this).hasClass('filtered_resource-visible')){
            $(this).removeClass("resource-hidden");
            $(this).addClass("resource-visible");
        }
        else{
            $(this).addClass("resource-hidden");
            $(this).removeClass("resource-visible");
        }
    });
    $(this).unbind('click');
    $(this).attr('class', 'resource_filter-hide');
    $(this).click(show_filtered_resources);
};

$('.resource_filter-hide').click(show_filtered_resources);
$('.resource_filter-show').click(hide_filtered_resources);
//xxxxxxxxxxxxxxxxxxxxxxxxxxEnd On Resource Filter Clickxxxxxxxxxxxxxxxxxxxxxxxx

//*******************************Edit Resource**********************************
$("#resource_edit_form #update_resource-btn").click(function(){
    var params = {'res_id': res_id};
    function success(resp) {
        resource_list[res_id]['name'] = params['name'];
        $("#edit_"+params['res_id']).text(params['name']);
        resource_list[res_id]['type'] = params['type'];
        resource_list[res_id]['short_description'] = params['short_description'];
        $("#short_description_"+params['res_id']).text(params['short_description']);
        resource_list[res_id].state = params.state
        resource_list[res_id].long_description = params.long_description;
        resource_list[res_id].accnt_code = params.accnt_code;
        resource_list[res_id].enabled = resource_list[res_id].enabled;
        resource_list[res_id].host_only = resource_list[res_id].host_only;
        resource_list[res_id].calc_mode = params.calc_mode;
        if(picture){
            resource_list[res_id]['picture'] = picture;
            $("#picture_"+res_id).show();
            $("#picture_"+res_id).attr('src', picture);
        }
        if(resource_list[res_id].calc_mode==calc_map.time_based)
            $("#clock_"+res_id).show();
        else
            $("#clock_"+res_id).hide();
        if((resource_list[res_id].flag & state) != state){
            $("#resource_"+res_id).removeClass("filtered_resource-visible");
            $("#resource_"+res_id).addClass("filtered_resource-hidden");
        }
        if(!$("#rtype_"+resource_list[res_id]['type']).hasClass('resource_type-show')){
            $("#resource_"+res_id).removeClass("typed_resource-visible");
            $("#resource_"+res_id).addClass("typed_resource-hidden");
        }
        if(!$("#resource_"+res_id).hasClass('typed_resource-visible') || !$("#resource_"+res_id).hasClass('filtered_resource-visible')){
            $("#resource_"+res_id).addClass("resource-hidden");
            $("#resource_"+res_id).removeClass("resource-visible");
        }
        $("#resource_list").show();
        $("#resource_filters").show();
        $("#resource_types").show();
        picture = null;
        view_resource_list();
    };
    function error() {
        $("#edit_resource-msg").text("Error in Updating Resource").addClass('status-fail');
    };
    params['name'] = $("#name").val();
    params['type'] = $("#type").val();
    params['short_description'] = $("#short_desc").val();
    params['long_description'] = $("#long_desc").val();
    params['accnt_code'] = $("#accnt_code").val();
    params['calc_mode'] = time_based_map[$("#time_based:checked").val()];
    params['enabled'] = checked_map[$("#state_enabled:checked").val()];
    params['host_only'] = checked_map[$("#state_host_only:checked").val()];
    if(picture)
        params['picture'] = picture;
    jsonrpc('resource.update', params, success, error); 
});

$("#resource_edit_form #cancel-btn").click( view_resource_list );

function resource_editing() {
    this_resource = resource_list[res_id];
    var name = this_resource.name;
    $('#res-profile-content').show();
    $("#content-title").text(name);
    $("#name").val(name);
    $("#type option[value='" + this_resource.type + "']").attr('selected', 'selected');
    $("#short_desc").val(this_resource.short_description);
    $("#long_desc").val(this_resource.long_description);
    $("#accnt_code").val(this_resource.accnt_code);
    $("#time_based").attr('checked', this_resource.calc_mode==calc_map.time_based);
    $("#state_enabled").attr('checked', this_resource.enabled);
    $("#state_host_only").attr('checked', this_resource.host_only);
};

function on_resource_pricings(resp) {
    this_res_pricing = resp.result;
    $('#price-tmpl').tmpl(this_res_pricing).appendTo('#current-prices');
    $('.text-xl').each( function() {
        $(this).text(format_currency($(this).text()));
    });
    $('#res-pricing-content').show();
};

function on_tariff_list(resp)  {
    $('#tariff-option-tmpl').tmpl(resp.result).appendTo('#tariff-select');
};

function on_tariff_pricings(resp) {
    $('#new-pricing').slideDown();
    $('#old-pricings').empty();
    $('#old-pricing-tmpl').tmpl(resp.result).appendTo('#old-pricings');
    $('.pricing-date').each( function() {
        $(this).text(isodate2fdate($(this).text()));
    });
    $('.pricing-amt').each( function() {
        $(this).text(format_currency($(this).text()));
    });
    $(".pricing .cancel-x").attr('href', window.location.hash);
    $(".pricing .cancel-x").click(delete_pricing);
    $(".pricing_edit-link").attr('href', window.location.hash);
    $(".pricing_edit-link").click(edit_pricing);
    $(".edit-cancel").click(cancel_edit_pricing);
    $(".edit-pricing").submit(save_edited_pricing);
};

function error(resp) {
    alert('error fetching pricings: ' + resp.error.message);
};

function get_pricing(id) {
    if (this_res_pricing == null) {
        var params = {'resource_id': id};
        jsonrpc('pricings.by_resource', params, on_resource_pricings, error);
        var params = {'owner': current_ctx};
        jsonrpc('tariffs.list', params, on_tariff_list, error);
    } else {
        $('#res-pricing-content').show();
    };
};

function load_tariff_pricings() {
    var params = {'resource_id': this_resource_id, 'tariff_id': $('#tariff-select').val()};
    jsonrpc('pricings.list', params, on_tariff_pricings, error);
};

$('#tariff-select').change( load_tariff_pricings );

$('#new-starts-vis').datepicker( {
    altFormat: 'yy-mm-dd',
    altField: '#new-starts',
    dateFormat: 'M d, yy'
});

function add_new_pricing() {
    var params = {'resource_id': this_resource_id, 'tariff_id': $('#tariff-select').val(), 'starts': $('#new-starts').val(), 
        'amount': $('#new-amount').val()};
    function error(resp) {
        alert('error adding new pricings: ' + resp.error.data);
    };
    function success () {};
    jsonrpc("pricings.new", params, load_tariff_pricings, error);
};

$('#new-pricing').submit(function () {
    $(this).checkValidity();
    add_new_pricing();
    return false;
});
function edit_pricing(){
    var pricing_id = $(this).attr('id').split('-')[1];
    $('#edit_starts_vis-'+pricing_id).datepicker( {
        altFormat: 'yy-mm-dd',
        altField: '#edit_starts-'+pricing_id,
        dateFormat: 'M d, yy'
    });
    var date = $("#pricing_date-"+pricing_id).text();
    if(date==""){
        $('#edit_starts_vis-'+pricing_id).replaceWith("<span id='#edit_starts-"+pricing_id+"'>-</span>");
    }
    else{
        $('#edit_starts_vis-'+pricing_id).datepicker("setDate", date);
    }
    $("#edit_amount-"+pricing_id).val(accounting.unformat($("#pricing_amount-"+pricing_id).text()));
    $("#pricing-"+pricing_id).hide();
    $("#edit_pricing-"+pricing_id).show();
};
function cancel_edit_pricing(){
    var pricing_id = $(this).attr('id').split('-')[1];
    $("#pricing-"+pricing_id).show();
    $("#edit_pricing-"+pricing_id).hide();
};
function save_edited_pricing(){
    var pricing_id = parseInt($(this).attr('id').split('-')[1], 10);
    $(this).checkValidity();
    function on_edit_error(resp) {
        alert('error updating pricings: ' + resp.error.data);
    };
    function on_edit_success () {
        load_tariff_pricings();
    };
    var params = {"pricing_id":pricing_id, "amount":$("#edit_amount-"+pricing_id).val()};
    var starts = $("#edit_starts-"+pricing_id).val();
    if(starts!="-")
        params['starts'] = starts;
    jsonrpc("pricing.update", params, on_edit_success, on_edit_error);
    return false;
};
function delete_pricing(){
    var pricing_id = $(this).attr('id').split('_')[1];
    function on_delete_pricing_error(resp) {
        alert('error deleting pricings: ' + resp.error.data);
    };
    function on_delete_pricing_success () {
        load_tariff_pricings();
    };
    jsonrpc("pricings.delete", {"pricing_id":pricing_id}, on_delete_pricing_success, on_delete_pricing_error);
};
//**************************Taxation**********************************************************
$("#tax_mode1").click(function(){
    $("#taxes_list *").removeAttr("disabled");
});
$("#tax_mode0").click(function(){
    $("#taxes_list *").attr("disabled", "disabled");
});
$("#add_tax-btn").click(function(){
    var data = {};
    data.name = $("#new_tax").val();
    data.value = $("#new_value").val();
    append_taxes([data]);
});
function append_taxes(data){
    $("#tax_tmpl").tmpl(data).appendTo("#taxes_list");
    $("#new_tax").val("");
    $("#new_value").val("");
    $(".remove-tax").unbind('click');
    $(".remove-tax A").attr("href", "#/"+res_id+"/edit/taxes");
    $(".remove-tax A").click(function(){
        $(this).parent().parent().remove();
    });
}
$("#taxation").submit(function(){
    $(this).checkValidity();
    update_taxes();
    return false;
});
function update_taxes(){
    params = {'res_id' : res_id};
    params.taxes = null;
    if(parseInt($("input:radio[name='tax_mode']:checked").val(), 10) == 0){
        params.taxes = null;
    }
    else{
        params.taxes = {};
        $('.new-tax').each(function(){
            params.taxes[$(".new-name", this).val()] =  parseFloat($(".new-value", this).val());    
        });
    }
    function on_taxes_updation_success(){
        $(".action-status").removeClass('status-fail');
        $(".action-status").text("Taxes saved successfully.").addClass('class', 'status-success');
    };
    function on_taxes_updation_error(){
        $(".action-status").removeClass('status-success');
        $(".action-status").text("Error in saving taxes.").addClass('class', 'status-fail');
    };
    jsonrpc("resource.update", params, on_taxes_updation_success, on_taxes_updation_error);  
};
function get_taxes(id) {
    if (this_res_taxes == null || res_id != id) {
        function on_get_taxes(resp){
            if(resp.result){
                $("#tax_mode1").click();
                var taxes = resp.result;
                for(var key in taxes){
                    append_taxes([{'name':key, 'value':taxes[key]}]);
                };
            }
            else{
                $("#tax_mode0").click();
            }
            this_res_taxes = true;
        };
        res_id = id;
        var params = {'res_id': id, 'attrname': 'taxes'};
        jsonrpc('resource.get', params, on_get_taxes, error);
    }
    $('#res-taxes-content').show();
};
setup_routing();
