$('#uninvoiced-start-vis').datepicker( {
    altFormat: 'yy-mm-dd',
    altField: '#uninvoiced-start',
    dateFormat: 'M d, yy'
});
$("#uninvoiced-start-vis").datepicker('setDate', new Date())

var uninvoiced_form = $('#uninvoiced-form');
var uninvoiced_form_status = $('#uninvoiced-form .action-status');

function on_receive_uninvoiced(resp) {
    var result = resp.result;
    uninvoiced_form_status.text('Invoices generation completed successfully').attr('class', 'status-success');
    $('#bill-template').tmpl(resp.result).appendTo('#bills-section')
    $('#invoicing-dashboard').slideUp('fast');
    $('#invoicing-actions').slideDown('fast');
    var start_date = null;
    var end_date = $('#uninvoiced-start').val();
    var po_number = null;
    for (var i=0; i < result.length; i++) {
        function on_invoice_gen(resp) {
            console.log(result);
            var invoice_id = resp.result;
            $('#view-invoice_' + result[i].member.id).show().attr('href', '/invoice/' + invoice_id + '/html');
        };
        var usages = [];
        for (var j=0; j < result[i].usages.length; j++) {
            usages.push(result[i].usages[j].id);
        };
        var params = {issuer: current_ctx, member: result[i].member.id, usages: usages, start_date: start_date , end_date: end_date, po_number:po_number}
        jsonrpc('invoice.new', params, on_invoice_gen, error, true);
    };
};

function request_uninvoiced() {
    var params = {res_owner_id: current_ctx};
    uninvoiced_form_status.text('generating invoices ...');
    var inputs = uninvoiced_form.serializeArray();
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
    };
    if (params.only_tariff == 'on') {
        params.only_tariff = true;
    } else {
        params.only_tariff = false;
    };
    function error(resp) {
        uninvoiced_form_status.text('Invoices generation failed').attr('class', 'status-fail');
    };
    jsonrpc('usages.uninvoiced_members', params, on_receive_uninvoiced, error);
};

uninvoiced_form.submit( function () {
    $(this).checkValidity();
    request_uninvoiced();
    return false;
});

