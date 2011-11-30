var day_miliseconds = 24 * 60 * 60 * 1000;
var resource_map = {};

function add_days(adate, days) {
    return new Date(adate.getTime() + (days * day_miliseconds))
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
    var resources = resp.result;
    $('#resource-opt').tmpl(resources).appendTo('#resource-select');
    for (idx in resources) {
        resource = resources[idx];
        resource_map[resource.id] = resource.name;
    };
};

$('#resource-select').change( function () {
    var resource_id = $(this).val();
    get_usages(resource_id);
    init_cal();
});

var params = {'owner': current_ctx};
jsonrpc("resources.available", params, on_available_resources, error);

$('#booking-date-inp').datepicker( {
    onSelect: set_day_titles
});

set_day_titles();

function id2datetime(id) {
    var slot_no = id.split('_')[1];
    var day_no = parseInt(slot_no.split('-')[0]);
    var time = slot_no.split('-')[1];
    return [day_no, time]
};

function on_select_slots(ev, ui) {
    var selected = [];
    $( ".ui-selected", this ).each( function () {
        selected.push($(this).attr('id'));
    });
    var start = selected[0];
    var end = start;
    var booking_day_no = id2datetime(start)[0];
    var start_time = id2datetime(start)[1];
    if (selected.length > 1) {
        end = selected.pop();
    };

    // arrghhh... javascript
    console.log(end);
    var end_time = new Date('2011-12-31T' + id2datetime(end)[1] + ':00')
    console.log(end_time);
    var end_time = new Date(end_time.getTime() + (15*60*1000))
    console.log(end_time);
    var end_time = to_iso_datetime(end_time).slice(-8,-3)
    console.log(end_time);

    var booking_date = add_days(get_selected_date(),  (-3 + booking_day_no))
    $('.data-resource-name').text(resource_map[$('#resource-select').val()]);
    $('#new-booking-date').text($.datepicker.formatDate('D, MM d, yy', get_selected_date()));
    $('#new-starts').val(start_time);
    $('#new-ends').val(end_time);
    $('#new-ends').attr('min', start_time);
    $('#booking-form').dialog({
        title: "New booking", 
        width: 500,
        height: 500
    });
};

function init_cal() {
    $(".cal-day").selectable({
        stop: on_select_slots
    });
};
