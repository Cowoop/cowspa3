//****************************Get Invoice History*******************************
function success(response) {
    $('#history_table').dataTable({
        "aaData": response['result'],
        "bJQueryUI": true,
        "sPaginationType": "full_numbers",
        "aoColumns": [
            { "sTitle": "ID" },
            { "sTitle": "MEMBER" },
            { "sTitle": "COST" },
            { "sTitle": "DATE" },
            { "sTitle": "Link",
              "fnRender": function(obj) {
                    var sReturn = obj.aData[obj.iDataColumn];
                    return "<A id='"+sReturn+"' href='#' class='invoice-view'>View</A>";
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
};
function error(){};
var params = { 'issuer' : current_ctx};
jsonrpc('invoice.history', params, success, error);
//xxxxxxxxxxxxxxxxxxxxxxxxxxxEnd Get Invoice Historyxxxxxxxxxxxxxxxxxxxxxxxxxxxx
