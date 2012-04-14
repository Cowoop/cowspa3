var history_table;
var invoice_to_send;
var invoice_email_text;
var send_status = $('#send_invoice-form .action-status');
//****************************Get Invoice History*******************************

function on_send_invoice_success() {
    function success() {
        invoice_to_send = null;
        $("#send-btn").removeAttr('disabled');
        window.location.reload();
    };
    send_status.removeClass('status-fail');
    send_status.addClass('status-success').text('Invoice sent successfully');
};

function on_send_invoice_failure() {
    send_status.removeClass('status-success');
    send_status.addClass('status-fail').text('failed to send invoice');
};


function rebind_actions() {

    var view_invoice_links = $('.view-invoice');

    view_invoice_links.unbind();
    view_invoice_links.click( function () {
        var invoice_id = $(this).attr('id').split('-')[1];
        $('#view_invoice_window #invoice-iframe').attr('src', '/invoice/'+ invoice_id +'/html');
        $('#view_invoice_window').dialog({
            title: "Invoice",
            width: 'auto'
        });
    });

    var send_invoice_links = $('.send-invoice');
    send_invoice_links.unbind();
    send_invoice_links.click(function () {
        $("#email_text").text(invoice_email_text);
        invoice_to_send = $(this).attr('id').split('-')[1];
        send_status.removeClass('status-fail');
        send_status.removeClass('status-success').text("");
        $('#send_invoice-form').dialog({ 
            title: "Send Invoice",
            width: 800
        });
    });

};

function on_get_invoices_success(response) {
    $('#invoice_row-tmpl').tmpl(response.result).appendTo('#history_table');
    history_table = $('#history_table').dataTable({
        "bJQueryUI": true,
        "bDestroy": true,
        "sPaginationType": "full_numbers",
        "aaSorting": [[ 3, "asc" ]],
        "aoColumnDefs": [
            {
                "fnRender": function( obj ) {
                    return isodate2fdate(obj.aData[3]) || "-";
                },
                "bUseRendered": false,
                "aTargets": [ 3 ]
            }
        ],
        "fnDrawCallback": function() {
            rebind_actions();
        }
    });

    $("#send-btn").click(function(){
        var params = {invoice_id : invoice_to_send, mailtext:$("#email_text").text()};
        send_status.text("Sending invoice.. please wait");
        $(this).attr('disabled', 'disabled');
        jsonrpc('invoice.send', params, on_send_invoice_success, on_send_invoice_failure);
    });

    $("#send_cancel-btn").click(function(){
        $('#send_invoice-form').dialog("close");
    });

    $('.delete-invoice').click(function () {
        var invoice_id = $(this).attr('id').split("-")[1];
        var row = $(this).closest("tr").get(0);
        function on_invoice_delete_success(){
            history_table.fnDeleteRow(history_table.fnGetPosition(row));
        };
        if(confirm("Do you want to delete invoice?")){
            jsonrpc("invoice.delete", {invoice_id: invoice_id}, on_invoice_delete_success);
        };
    });
};

jsonrpc('invoice.list', {issuer: current_ctx, limit: 1000}, on_get_invoices_success);

function on_get_invoicemail_cust(response) {
    invoice_email_text = response.result;
};

jsonrpc('messagecust.get', {owner_id: current_ctx, name: 'invoice'}, on_get_invoicemail_cust);
