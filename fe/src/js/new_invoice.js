$('#invoicee-search').autocomplete({
    source: "/search_members",
    select: function(event, ui) {
        var params = {member_id: ui.item.id};
        function success (response) {
            var data = response['result'];
            data.id = ui.item.id;
            $('#invoicee-info-tmpl').tmpl(data).appendTo('#invoicee-info');
            $('#invoicee-info').show();
        };
        function error () {};
        jsonrpc('member.contact', params, success, error);
    }
});

$('#new-usage-form #start').datetimepicker({
    timeFormat: 'h:m',
    dateFormat: 'dd.mm.yy',
});
$('#new-usage-form #end').datetimepicker({
    timeFormat: 'h:m',
});
$('#new-usage-button').click(function() {
    $('#new-usage-form').dialog({ title: "Create new usage", width: 500});
});
$('#submit-usage').click( function () {
    var params = $('#new-usage-form').serializeArray();
    var data = {};
    $.each(params, function(idx, v) {
        data[v.name] = v.value;
    });
    data.total = data.quantity * data.rate;
    $('#usage-tmpl').tmpl([data]).appendTo('#usages');
    $('#new-usage-form').dialog('close');
});

