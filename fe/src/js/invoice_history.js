var history_table;
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
                    var sReturn = obj.aData[obj.iDataColumn];
                    return "<A id='"+sReturn+"' href='#' class='invoice-view'>View</A>|<A id='delete-"+sReturn+"' href='#' class='invoice-delete'>X</A>";
                    }
            }
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
};
function error(){};
var params = { 'issuer' : current_ctx};
jsonrpc('invoice.list', params, success, error);
//xxxxxxxxxxxxxxxxxxxxxxxxxxxEnd Get Invoice Historyxxxxxxxxxxxxxxxxxxxxxxxxxxxx
