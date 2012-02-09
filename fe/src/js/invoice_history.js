var history_table;
var invoice_send_link_id, invoice_no_column_id;
var invoice_email_text;
//****************************Get Invoice History*******************************
function on_get_invoices_success(response) {
    history_table = $('#history_table').dataTable({
        "aaData": response['result'],
        "bJQueryUI": true,
        "bDestroy": true,
        "sPaginationType": "full_numbers",
        "aaSorting": [[ 0, "desc" ]],
        "aoColumns": [
            { "sTitle": "Number",
              "fnRender": function(obj) {
                    var number = obj.aData[obj.iDataColumn];
                    return number?number:"-";
                    }
            },
            { "sTitle": "Member" },
            { "sTitle": "Cost",
              "fnRender": function(obj) {
                    var cost = format_currency(obj.aData[ obj.iDataColumn ]);
                    return cost;
                    }
            },
            { "sTitle": "Date",
              "fnRender": function(obj) {
                    var sReturn = obj.aData[obj.iDataColumn];
                    return isodate2fdate(sReturn);
                    }   
            },
            { "sTitle": "Send",
              "fnRender": function(obj) {
                    var sent = obj.aData[obj.iDataColumn];
                    var inv_id = obj.aData[obj.iDataColumn+1];
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
            { "sTitle": "Actions", "bSortable": false,
              "fnRender": function(obj) {
                    var sent = obj.aData[obj.iDataColumn-1];
                    var inv_id = obj.aData[obj.iDataColumn];
                    var link;
                    if(sent){
                        link = "<A id='"+inv_id+"' href='#' class='invoice-view'>View</A>";
                    }
                    else{
                        link = "<A id='"+inv_id+"' href='#' class='invoice-view'>View</A>|<A id='delete-"+inv_id+"' href='#' class='invoice-delete'>X</A>";
                    };
                    return link;
                    }
            },
        ]
    });
    $('<DIV>Note: Only sent Invoices has Invoice Number.</DIV>').insertAfter("#history_table_info");
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
        if(confirm("Do you want to delete invoice?")){
            jsonrpc("invoice.delete", {'invoice_id':$(this).attr('id').split("-")[1]}, on_invoice_delete_success);
        };
    });
    //xxxxxxxxxxxxxxxxxxxxxxxxxxEnd Delete Invoicexxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    //****************************Send Invoice**********************************
    $('.inv-send').click(function () {
        $("#email_text").text(invoice_email_text);
        invoice_send_link_id = $(this).attr("id");
        invoice_no_column_id = $(this).parent().parent().children(":first-child");
        $('#send_invoice-form').dialog({ 
            title: "Send Invoice" 
        });
    });
    function on_send_invoice_success() {
        $("#"+invoice_send_link_id).text("Resend");
        params['attr'] = 'number';
        function on_get_number_success(resp){
            $(invoice_no_column_id).text(resp.result);
        }
        jsonrpc('invoice.get', params, on_get_number_success);
    };
    $("#send-btn").click(function(){
        var params = {invoice_id : invoice_send_link_id.split("-")[1], mailtext:$("#email_text").text()};
        jsonrpc('invoice.send', params, on_send_invoice_success);
    });
    $("#send_cancel-btn").click(function(){
        $('#send_invoice-form').dialog("close"); ;
    });
    //xxxxxxxxxxxxxxxxxxxxxxxxxxEnd Delete Invoicexxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
};
jsonrpc('invoice.list', {issuer: current_ctx}, on_get_invoices_success);

//xxxxxxxxxxxxxxxxxxxxxxxxxxxEnd Get Invoice Historyxxxxxxxxxxxxxxxxxxxxxxxxxxxx
//******************************Email text************************************

function on_get_invoicemail_cust(response) {
    invoice_email_text = response.result;
};

jsonrpc('messagecust.get', {owner_id: current_ctx, name: 'Invoice'}, on_get_invoicemail_cust);
