var history_table;
var inv_id, sent;
var box_id, number_td;
var email_text;
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
            { "sTitle": "Cost" },
            { "sTitle": "Date",
              "fnRender": function(obj) {
                    var sReturn = obj.aData[obj.iDataColumn];
                    return isodate2fdate(sReturn);
                    }   
            },
            { "sTitle": "Send",
              "fnRender": function(obj) {
                    sent = obj.aData[obj.iDataColumn];
                    inv_id = obj.aData[obj.iDataColumn+1];
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
        function on_invoice_delete_error(resp){
            alert("Error in deleting invoice: "+resp.error.data);
        };
        if(confirm("Do you want to delete invoice?")){
            jsonrpc("invoice.delete", {'invoice_id':$(this).attr('id').split("-")[1]}, on_invoice_delete_success, on_invoice_delete_error);
        };
    });
    //xxxxxxxxxxxxxxxxxxxxxxxxxxEnd Delete Invoicexxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    //****************************Send Invoice**********************************
    $('.inv-send').click(function () {
        $("#email_text").text(email_text);
        box_id = $(this).attr("id");
        number_td = $(this).parent().parent().children(":first-child");
        function on_send_invoice_success() {
            $("#"+box_id).text("Resend");
            alert('Invoice sent successfully');
            params['attr'] = 'number';
            function on_get_number_success(resp){
                $(number_td).text(resp.result);
            }
            jsonrpc('invoice.get', params, on_get_number_success, on_send_invoice_failure);
        };
        function on_send_invoice_failure() {
            alert('failed to send invoice');
        };
        $('#send_invoice-form').dialog({ 
            title: "Send Invoice", 
            width: 500, 
        });
        $("#send-btn").click(function(){
            var params = {invoice_id : box_id.split("-")[1], mailtext:$("#email_text").text()};
            jsonrpc('invoice.send', params, on_send_invoice_success, on_send_invoice_failure);
        });
        $("#send_cancel-btn").click(function(){
            $('#send_invoice-form').dialog("close"); ;
        });
    });
    //xxxxxxxxxxxxxxxxxxxxxxxxxxEnd Delete Invoicexxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
};
function error(){};
var params = { 'issuer' : current_ctx};
jsonrpc('invoice.list', params, on_get_invoices_success, error);
//xxxxxxxxxxxxxxxxxxxxxxxxxxxEnd Get Invoice Historyxxxxxxxxxxxxxxxxxxxxxxxxxxxx
//******************************Email text************************************
function on_get_invoicepref_success(response) {
    email_text = response['result']['email_text'];
};
function on_get_invoicepref_error(){};
jsonrpc('invoicepref.info', { 'owner' : current_ctx}, on_get_invoicepref_success, on_get_invoicepref_error);
