var tariff_baseurl =  basepath + '/tariffs/';
var tariff_id = null;
var action_status = $('#tariff_form .action-status');
var tariffs_title = $('#content-title').text();
var tariff_pricing = null;

function update_tariff(theform) {
    var inputs = theform.serializeArray();
    var params = {}
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
    }
    function success() {
        action_status.text("Tariff Updated successfully.").attr('class', 'status-success');
        setTimeout(function(){
            window.location = tariff_baseurl;
        }, 1000);
    };
    function error() {
        action_status.text("Error while Updating Tariff.").attr('class', 'status-fail');
    };
    params['owner'] = current_ctx;
    params['type'] = 'tariff';
    params['res_id'] = tariff_id;
    jsonrpc('resource.update', params, success, error);
}

$("#cancel-btn").click(function (){
    $("#tariff_form").hide();
    $("#tariff-pricing-content").hide();
    $("#new-tariff").show();
    $("#tariff_list").show();
    $('#content-title').text(tariffs_title);
    window.location = tariff_baseurl;
});

$('#new-starts-vis').datepicker( {
    altFormat: 'yy-mm-dd',
    altField: '#new-starts',
    dateFormat: 'M d, yy'
});

function add_new_pricing() {
    var params = {'owner': current_ctx, 'tariff_id': tariff_id, 'starts': $('#new-starts').val(), 
        'amount': $('#new-amount').val()};
    function error(resp) {
        alert('error adding new pricings: ' + resp.error.data);
    };
    function success () {
        $('#new-amount').val('');
        $('#new-starts-vis').val('');
        get_pricing(tariff_id);
    };
    jsonrpc("pricings.new_tariff", params, success, error);
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
function allow_edit_pricing(pricing_id){
    //var pricing_id = $(this).attr('id').split('-')[1];
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
        $("#pricing_amount-"+pricing_id).text(format_currency($("#edit_amount-"+pricing_id).val()));
        allow_edit_pricing(pricing_id);
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
        get_pricing(tariff_id);
    };
    if ($('#pricing_date-'+pricing_id).html() == "") {
        alert('Price without start date not allowed to be deleted');
    } else {
        if(confirm("Do you want to remove?")){
            jsonrpc("pricings.delete", {"pricing_id":pricing_id}, on_delete_pricing_success, on_delete_pricing_error);
        }
    }
};
function on_tariff_pricing(resp) {
    tariff_pricing = resp.result;
    $('#old-pricings').empty();
    $('#old-pricing-tmpl').tmpl(resp.result).appendTo('#old-pricings');
    $('.pricing-amt').each( function() {
        $(this).text(format_currency($(this).text()));
    });
    $(".pricing .cancel-x").attr('href', window.location.hash);
    $(".pricing .cancel-x").click(delete_pricing);
    $(".pricing_edit-link").attr('href', window.location.hash);
    $(".pricing_edit-link").click(edit_pricing);
    $(".edit-cancel").click(allow_edit_pricing);
    $(".edit-pricing").submit(save_edited_pricing);
};

function get_pricing(id) {
    function error(resp) {
        alert('error fetching pricing: ' + resp.error.data);
    };

    var params = {'tariff': id, 'owner': current_ctx};
    jsonrpc('pricings.default_tariff', params, on_tariff_pricing, error);
};

function show_editform(id) {
    if (tariff_pricing == null) {
        get_pricing(id);
    }

    $("#tariff_list").hide();
    $("#tariff_form").show();
    $("#tariff-pricing-content").show();

    function success(resp) {
        tariff = resp['result'];
        $('#content-title').text(tariff.name);
        $('#tariff_form #name').val(tariff.name);
        $('#tariff_form #short_description').val(tariff.short_description);
    };

    function error() {
        alert('Unable to get Tariff Information');
    };

    var params = {'res_id': id};
    jsonrpc('resource.info', params, success, error);
}

function act_on_route(id) {
    if (tariff_id != id) {
        tariff_id = id;
    }
};

function setup_routing () {
    var routes = {
        '/:id': {
            '/edit': show_editform,
            on: act_on_route
        },
    };

    Router(routes).configure({ recurse: 'forward' }).init();
};

setup_routing();

$(document).ready(function() {
    var params = {}
    function success(resp) {
//        var markup = "<div class='tariff-box'><div class='tariff-title'>${name}</div> ${short_description}</div>";
//        $.template( "tariffTemplate", markup );
        no_tariffs = resp['result'].length;
        $('#tariff_tmpl').tmpl(resp['result'].slice(0,no_tariffs/2)).appendTo( "#tariff_list #left" );
        $('#tariff_tmpl').tmpl(resp['result'].slice(no_tariffs/2)).appendTo( "#tariff_list #right" );
        };
    function error() {
        };
    params['owner'] = current_ctx;
    jsonrpc('tariffs.list', params, success, error);
});

$("#new-tariff").click(function (){
    window.location = basepath + '/tariff/new'
});

$('#tariff_form').submit(function () {
    var theform = $(this);
    theform.checkValidity();
    update_tariff(theform);
    return false;
});
