function on_get_member_list_success(response) {
	$('#member_table').dataTable({
		"sDom": 'T<"clear">lfrtip',
		"oTableTools": {
		    "sSwfPath": "/swf/copy_cvs_xls_pdf"
		},
		"aaData": response.result,
        "bJQueryUI": true,
        "bDestroy": true,
        "sPaginationType": "full_numbers",
        "aaSorting": [[ 1, "asc" ]],
        "aoColumns": [
                { "sTitle": "ID", "sWidth": "20%" },
                { "sTitle": "Name", "sWidth": "40%"},
                { "sTitle": "Email", "sWidth": "40%" }
                ]
	});
};
jsonrpc('member.list', {formember_id: current_userid, bizplace_ids: [current_ctx], hashrows: false}, on_get_member_list_success);
