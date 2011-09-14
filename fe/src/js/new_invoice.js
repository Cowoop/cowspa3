var inv_usages = [];
var inv_id = null;
var inv_member_id = null;

$('#invoicee-search').autocomplete({
    source: "/search_members",
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

$('#new-usage-form #start_time').datetimepicker({
    timeFormat: 'h:m',
    dateFormat: 'dd.mm.yy',
});
$('#new-usage-form #end_time').datetimepicker({
    timeFormat: 'h:m',
});
$('#new-usage-button').click(function() {
    $('#new-usage-form').dialog({ title: "Create new usage", width: 500});
});
$('#submit-usage').click( function () {
    var params = $('#new-usage-form').serializeArray();
    var data = {};
    $.each(params, function(idx, v) {
        data[v.name] = v.value;
    });
    data.calculated_cost = (data.quantity * data.rate);
    data.id = inv_usages.push(data);
    $('#usage-tmpl').tmpl([data]).appendTo('#usages');
    $('#new-usage-form').dialog('close');
});
function on_create_invoice(response) {
    inv_id = response.result;
    $('#inv-action-status').text('Invoice creation successful');
    $('#inv-action-status').attr('class', 'status-success');
    $('#invoice-save').attr("disabled", true);
    $('#invoice-view').removeAttr("disabled");
    $('#invoice-send').removeAttr("disabled");
    $('#view_invoice_window #invoice-iframe').attr('src', '/invoices/'+inv_id+'/html');
};
function on_create_invoice_failure() {
    $('#inv-action-status').text('failed to create invoice');
};
$('#invoice-save').click( function () {
    var new_usages = [];
    $.each(inv_usages, function(idx, v) {
        var o = v;
        delete o.id;
        delete o.unit;
        new_usages.push(o)
    });
    var params = {issuer: current_bizplace, member: inv_member_id, po_number: $('#po_number').val(), new_usages: new_usages, start_date: $('#inv-start_date').val(), end_date: $('#inv-end_date').val()};
    jsonrpc('invoice.new', params, on_create_invoice, on_create_invoice_failure);
});
$('#invoice-view').click(function () {
    $('#view_invoice_window').dialog({ 
        title: "Invoice", 
        width: 500,
        height: 500
    });
});
