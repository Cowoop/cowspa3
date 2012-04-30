function on_get_member_list_success(response) {
    var data = response.result;
    var aaData = [];
    for (var i=0; i < data.length; i++) {
        var item = data[i];
        aaData.push([item.name, item.number, item.tariff_name, item.email]);
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
            { "sTitle": "Name", "sWidth": "25%" },
            { "sTitle": "Membership No", "sWidth": "25%"},
            { "sTitle": "Membership", "sWidth": "25%" },
            { "sTitle": "Email", "sWidth": "25%",
                "fnRender": function(obj) {
                    var email = obj.aData[obj.iDataColumn];
                    return "<A href='mailto:"+email+"'>"+email+"</A>";
                    }
            }
            ]
    });
};
jsonrpc('roles.members_by_roles', {context: current_ctx}, on_get_member_list_success);
