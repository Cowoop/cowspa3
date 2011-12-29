var history_table;
var inv_id;
//****************************Get Invoice History*******************************
function success(response) {
    history_table = $('#history_table').dataTable({
        "aaData": response['result'],
        "bJQueryUI": true,
        "sPaginationType": "full_numbers",
        "aoColumns": [
            { "sTitle": "Number" },
            { "sTitle": "Member" },
            { "sTitle": "Cost" },
            { "sTitle": "Date",
              "fnRender": function(obj) {
                    var sReturn = obj.aData[obj.iDataColumn];
                    return to_formatted_date(sReturn);
                    }   
            },
            { "sTitle": "Link", "bSortable": false,
              "fnRender": function(obj) {
                    var id = obj.aData[obj.iDataColumn];
                    inv_id = id;
                    return "<A id='"+id+"' href='#' class='invoice-view'>View</A>|<A id='delete-"+id+"' href='#' class='invoice-delete'>X</A>";
                    }
            },
            { "sTitle": "Send",
              "fnRender": function(obj) {
                    var sent = obj.aData[obj.iDataColumn];
                    var link;
                    if(sent){
                        link = "<A id='inv-"+inv_id+"' href='#' class='inv-send'>Resend</A>";
                    }
                    else{
                        link = "<A id='inv-"+inv_id+"' href='#' class='inv-send'>Send</A>";
                    }
                    return link;
                    }   
            },
        ]
    });
    //****************************View Invoice**********************************
    $('.invoice-view').click(function () {
        $('#view_invoice_window #invoice-iframe').attr('src', '/invoice/'+$(this).attr('id')+'/html');
        $('#view_invoice_window').dialog({ 
            title: "Invoice", 
            width: 800,
            height: 600
         });
    });
    //xxxxxxxxxxxxxxxxxxxxxxxxxxEnd View Invoicexxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    //****************************Delete Invoice**********************************
    $('.invoice-delete').click(function () {
        var row = $(this).closest("tr").get(0);
        function on_invoice_delete_success(){
            history_table.fnDeleteRow(history_table.fnGetPosition(row));
        };
        function on_invoice_delete_error(resp){
            alert("Error in deleting invoice");
        };
        jsonrpc("invoice.delete", {'invoice_id':$(this).attr('id').split("-")[1]}, on_invoice_delete_success, on_invoice_delete_error);
    });
    //xxxxxxxxxxxxxxxxxxxxxxxxxxEnd Delete Invoicexxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    //****************************Send Invoice**********************************
    $('.inv-send').click(function () {
        var box_id = $(this).attr("id");
        function on_send_invoice() {
            $("#"+box_id).text("Resend");
            alert('Invoice sent successfully');
        };
        function on_send_invoice_failure() {
            alert('failed to send invoice');
        };
        var params = {invoice_id : box_id.split("-")[1]};
        jsonrpc('invoice.send', params, on_send_invoice, on_send_invoice_failure);
    });
    //xxxxxxxxxxxxxxxxxxxxxxxxxxEnd Delete Invoicexxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
};
function error(){};
var params = { 'issuer' : current_ctx};
jsonrpc('invoice.list', params, success, error);
//xxxxxxxxxxxxxxxxxxxxxxxxxxxEnd Get Invoice Historyxxxxxxxxxxxxxxxxxxxxxxxxxxxx
