var day_miliseconds = 24 * 60 * 60 * 1000;
var resource_map = {};
var shown_dates = [];

function add_days(adate, days) {
    return new Date(adate.getTime() + (days * day_miliseconds))
};

function set_day_titles() {
    var date_selected = get_selected_date();
    $('.day-title').each( function (idx) {
        var date_next = add_days(date_selected, (idx - 3));
        var date_text = $.datepicker.formatDate('D d', date_next)
        $(this).text(date_text);
        shown_dates[idx] = date_next;
    });
};

$('#booking-date-inp').datepicker( {
    onSelect: set_day_titles
});

function get_selected_date() {
    return new Date($('#booking-date-inp').val());
};

function error(resp) {
    alert('Remote error: ' + resp.result.message);
};

function on_get_usages(resp) {
    mark_slots(resp.result);
    init_cal();
};

function get_usages(resource_id) {
    params = {'resource_ids': [resource_id],
        'start': add_days(get_selected_date(), -3),
        'end': add_days(get_selected_date(), 3)
    };
    jsonrpc("usages.find", params, on_get_usages, error);
};

function mark_slot(usage) {
    var start_time = new Date(usage.start_time);
    var end_time = new Date(usage.end_time);
    for (i in shown_dates) {
        if (shown_dates[i] >= start_time) {
            break;
        };
    };
    var matched_day_idx = i-1;
    var day_id = 'day_' + matched_day_idx;

    var matched_slots = [];

    var this_time = new Date(start_time.getFullYear(), start_time.getMonth(), start_time.getDate())
    $('#' + day_id + ' .cal-min15').each( function () {
        var this_id = $(this).attr('id');
        var [this_hh, this_mm] = this_id.split('-')[1].split('.')[0].split(':');
        this_time.setHours(this_hh);
        this_time.setMinutes(this_mm);
        this_time.setSeconds(0);
        this_time.setMilliseconds(0);
        if ((this_time >= start_time) && (this_time <= end_time)) {
            $(this).addClass('slot-unavailable');
            $(this).removeClass('slot-available');
            matched_slots.push(this);
        };
    });
};

function mark_slots(usages) {
    for (i in usages) {
        mark_slot(usages[i]);
    };
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

set_day_titles();

function id2datetime(id) {
    var slot_no = id.split('_')[1];
    var day_no = parseInt(slot_no.split('-')[0]);
    var [start, end] = slot_no.split('-')[1].split('.');
    return [day_no, start, end]
};

function on_select_slots(ev, ui) {
    var selected = [];
    $( ".ui-selected", this ).each( function () {
        selected.push($(this).attr('id'));
    });
    var start = selected[0];
    var end = selected.pop();
    var [booking_day_no, start_time] = id2datetime(start);
    var end_time = id2datetime(end)[2];

    var booking_date = add_days(get_selected_date(),  (-3 + booking_day_no))
    var resource_name = resource_map[$('#resource-select').val()];
    $('.data-resource-name').text(resource_name);
    $('#new-booking-date').text($.datepicker.formatDate('D, MM d, yy', booking_date));
    $('#new-starts').val(start_time);
    $('#new-ends').val(end_time);
    $('#new-ends').attr('min', start_time);
    $('#booking-form').dialog({
        title: resource_name,
        width: 500,
        height: 500
    });
};

function init_cal() {
    $(".cal-day").selectable({
        cancel: '.slot-unavailable',
        stop: on_select_slots
    });
    $('#booking-cal').removeClass('opaq');
};
