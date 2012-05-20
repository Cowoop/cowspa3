var headers = ["Name", "Membership No.", "Tariff", "Mobile", "Email"]

function on_get_member_list_success(response) {
    var data = response.result[1];
    var aaData = [];
    for (var i=0; i < data.length; i++) {
        var item = data[i];
        aaData.push([item[1] + ' ' + item[2], item[3], item[6], item[4], item[5]]);
    };

    $('#member_table').dataTable({
    	"sDom": '<"H"lT>rt<"F"ip>',
    	"oTableTools": {
    	    "sSwfPath": "/swf/copy_cvs_xls_pdf"
    	},
    	"aaData": aaData,
    "bJQueryUI": true,
    "bDestroy": true,
    "sPaginationType": "full_numbers",
    "aaSorting": [[ 0, "asc" ]],
    "aoColumns": [
            { "sTitle": headers[0], "sWidth": "25%" },
            { "sTitle": headers[1], "sWidth": "15%" },
            { "sTitle": headers[2], "sWidth": "20%"},
            { "sTitle": headers[3], "sWidth": "20%" },
            { "sTitle": headers[4], "sWidth": "20%",
                "fnRender": function(obj) {
                    var email = obj.aData[obj.iDataColumn];
                    return "<A href='mailto:"+email+"'>"+email+"</A>";
                    }
            }
            ]
    });
    on_render_table();
};

function on_render_table() {
};

jsonrpc('members.export', {context: current_ctx}, on_get_member_list_success);
