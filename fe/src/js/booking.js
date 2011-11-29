var day_miliseconds = 24 * 60 * 60 * 1000;

function add_days(adate, days) {
    return new Date(adate.getTime() + (days * day_miliseconds))
};

function sevendays(adate) {
    var days = [];
    for (var i=0;  i<= 6; i++) {
        days[i] = add_days(adate, 1);
    };
    return days;
};

function get_selected_date() {
    return new Date($('#booking-date-inp').val());
};

function set_day_titles() {
    var date_selected = get_selected_date();
    $('.day-title').each( function (idx) {
        var date_next = add_days(date_selected, (idx - 3));
        var date_text = $.datepicker.formatDate('D d', date_next)
        $(this).text(date_text);
    });
};

function error(resp) {
    alert('Remote error: ' + resp.result.message);
};

function on_get_usages(resp) {
    mark_slots();
    init_cal();
};

function get_usages(resource_id) {
    params = {'resource_ids': [resource_id],
        'start': add_days(get_selected_date(), -3),
        'end': add_days(get_selected_date(), 3)
    };
    jsonrpc("usages.find", params, on_get_usages, error);
};

function mark_slots() {
};

function on_available_resources(resp) {
    tariffs = resp.result;
    $('#resource-opt').tmpl(tariffs).appendTo('#resource-select');
};

$('#resource-select').change( function () {
    var resource_id = $(this).val();
    get_usages(resource_id);
});

var params = {'owner': current_ctx};
jsonrpc("resources.available", params, on_available_resources, error);

$('#booking-date-inp').datepicker( {
    onSelect: set_day_titles
});

set_day_titles();

function init_cal() {
    $(".cal-day").selectable({
        selected: function () {  }
    });
};

$('#booking-date-inp-vis').change ( function () {
    alert(1);
});
