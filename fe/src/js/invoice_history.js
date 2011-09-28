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
                    return "<A href='/invoice/"+sReturn+"/html'>View</A>";
                    }
            }
        ]
    });
};
function error(){};
var params = { 'issuer' : current_bizplace};
jsonrpc('invoice.history', params, success, error);
//xxxxxxxxxxxxxxxxxxxxxxxxxxEnd Get Invoice Historyxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

