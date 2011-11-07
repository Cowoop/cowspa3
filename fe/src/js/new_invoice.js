var inv_usages = [];
var inv_id = null;
var inv_member_id = null;
var custom_resource = false;

$('#invoicee-search').autocomplete({
    source: "/search/members",
    select: function(event, ui) {
        var params = {member_id: ui.item.id};
        function success (response) {
            var data = response['result'];
            data.id = ui.item.id;
            inv_member_id = data.id;
            $('#invoicee-info-tmpl').tmpl(data).appendTo('#invoicee-info');
            $('#invoicee-info').show();
        };
        function error () {};
        jsonrpc('member.contact', params, success, error);
    }
});

$('#inv-start_date-vis').datepicker( {
    altFormat: 'yy-mm-dd',
    altField: '#inv-start_date',
    dateFormat: 'M d, yy'
});
$('#inv-end_date-vis').datepicker( {
    altFormat: 'yy-mm-dd',
    altField: '#inv-end_date',
    dateFormat: 'M d, yy'
});

// altFormat does not work with timepicker :-(
// https://github.com/trentrichardson/jQuery-Timepicker-Addon/issues/94

$('#new-usage-form #start_time').datetimepicker({
    ampm: true,
    dateFormat: 'M d, yy',
    timeFormat: 'hh:mm tt',
});
$('#new-usage-form #end_time').datetimepicker({
    ampm: true,
    dateFormat: 'M d, yy',
    timeFormat: 'hh:mm tt',
});
$('#new-usage-button').click(function() {
    $("#resource_select").show();
    $("#resource_name").hide();
    $("#custom").show();
    custom_resource = false;
    $('#new-usage-form').dialog({ title: "Create new usage", width: 500});
});
$('#submit-usage').click( function () {
    var params = $('#new-usage-form').serializeArray();
    var data = {}; 
    $.each(params, function(idx, v) {
        data[v.name] = v.value;
    });
    if(!custom_resource){
        data.resource_name = data.resource_select;
    }
    delete(data.resource_select);
    data.calculated_cost = (data.quantity * data.rate);
    data.id = inv_usages.push(data);
    $('#usage-tmpl').tmpl([data]).appendTo('#usages');
    $(".cancel-usage").click(function(){
        if(confirm("Do you want to remove?")){
            var usage_id = parseInt($(this).attr('id').split('-')[1]);
            $(this).parent().parent().remove();
            delete(inv_usages[usage_id-1]);
        }
    });
    $('#new-usage-form').dialog('close');
});
function on_create_invoice(response) {
    inv_id = response.result;
    $('#inv-action-status').text('Invoice creation successful');
    $('#inv-action-status').addClass('status-success');
    $('#invoice-save').attr("disabled", true);
    $('#invoice-view').removeAttr("disabled");
    $('#invoice-send').removeAttr("disabled");
    $('#view_invoice_window #invoice-iframe').attr('src', '/invoice/'+inv_id+'/html');
};
function on_create_invoice_failure() {
    $('#inv-action-status').text('failed to create invoice');
    $('#inv-action-status').addClass('status-fail');
};
$('#invoice-save').click( function () {
    var new_usages = [];
    $.each(inv_usages, function(idx, v) {
        if(v != undefined){
            var o = v;
            delete o.id;
            delete o.unit;
            o.start_time = to_iso_datetime(o.start_time);
            o.end_time = to_iso_datetime(o.end_time);
            new_usages.push(o)
        }
    });
    var params = {issuer: current_ctx, member: inv_member_id, po_number: $('#po_number').val(), notice: $('#notice').val(), new_usages: new_usages, start_date: $('#inv-start_date').val(), end_date: $('#inv-end_date').val()};
    jsonrpc('invoice.new', params, on_create_invoice, on_create_invoice_failure);
});
$('#invoice-view').click(function () {
    $('#view_invoice_window').dialog({ 
        title: "Invoice", 
        width: 800,
        height: 600
    });
});
$('#invoice-send').click(function () {
    $('#inv-action-status').text('sending ...');
    function on_send_invoice() {
        $('#inv-action-status').text('Invoice sent successfully');
    };
    function on_send_invoice_failure() {
        $('#inv-action-status').text('failed to send invoice');
        $('#inv-action-status').addClass('status-fail');
    };
    var params = {invoice_id : inv_id};
    jsonrpc('invoice.send', params, on_send_invoice, on_send_invoice_failure);
});
//****************************Get Resources*************************************
function on_get_resources_success(res) {
    $('#resource-tmpl').tmpl(res['result']).appendTo('#resource_select');
};
function on_get_resources_error(){};
jsonrpc('resource.list', {'owner':current_ctx}, on_get_resources_success, on_get_resources_error);
//xxxxxxxxxxxxxxxxxxxxxxxxxxxEnd Get Resourcesxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
$("#custom").click(function(){
    $("#resource_select").hide();
    $("#resource_name").show();
    $(this).hide();
    custom_resource = true;
});

