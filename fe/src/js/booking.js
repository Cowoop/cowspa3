var day_miliseconds = 24 * 60 * 60 * 1000;
var resource_map = {};
var shown_dates = [];
var new_booking_date = null;

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
        'start': to_iso_date(add_days(get_selected_date(), -3)),
        'end': to_iso_date(add_days(get_selected_date(), 3))
    };
    jsonrpc("usages.find", params, on_get_usages, error);
};

function mark_slot(usage) {
    var start_time = iso2date(usage.start_time);
    var end_time = iso2date(usage.end_time);
    for (i in shown_dates) {
        if (shown_dates[i] >= start_time) {
            break;
        };
    };
    var matched_day_idx = i;
    var day_id = 'day_' + matched_day_idx;

    var matched_slots = [];

    var this_time = new Date(start_time.getFullYear(), start_time.getMonth(), start_time.getDate());
    $('#' + day_id + ' .cal-min15').each( function () {
        var this_id = $(this).attr('id');
        var hh_mm = this_id.split('-')[1].split('.')[0].split(':');
        var this_hh = hh_mm[0];
        var this_mm = hh_mm[1];
        this_time.setHours(this_hh);
        this_time.setMinutes(this_mm);
        this_time.setSeconds(0);
        this_time.setMilliseconds(0);
        if ((this_time >= start_time) && (this_time < end_time)) {
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
    refresh_cal();
});

var params = {'owner': current_ctx};
jsonrpc("resources.available", params, on_available_resources, error);

set_day_titles();

function id2datetime(id) {
    var slot_no = id.split('_')[1];
    var day_no = parseInt(slot_no.split('-')[0]);
    var start_end = slot_no.split('-')[1].split('.');
    var start = start_end[0];
    var end = start_end[1];
    return [day_no, start, end]
};

function on_select_slots(ev, ui) {
    var selected = [];
    $( ".ui-selected", this ).each( function () {
        selected.push($(this).attr('id'));
    });
    var start = selected[0];
    var end = selected.pop();
    var no_start = id2datetime(start);
    var booking_day_no = no_start[0];
    var start_time = no_start[1];
    var end_time = id2datetime(end)[2];

    new_booking_date = add_days(get_selected_date(),  (-3 + booking_day_no))
    var resource_name = resource_map[$('#resource-select').val()];
    $('.data-resource-name').text(resource_name);
    $('#new-booking-date').text($.datepicker.formatDate('D, MM d, yy', new_booking_date));
    $('#new-starts').val(start_time);
    $('#new-ends').val(end_time);
    $('#new-ends').attr('min', start_time);
    $('#new-booking').dialog({
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

function refresh_cal() {
    $(".cal-day").selectable('destroy');
    $('.slot-unavailable').each( function () {
        $(this).removeClass('slot-unavailable');
        $(this).removeClass('slot-available');
    });
    get_usages(parseInt($('#resource-select').val()));
};

$('#for-member-search').autocomplete({
    source: "/search/member",
    select: function(event, ui) {
        $('#for-member').val(ui.item.id);
    }
});

function on_new_booking() {
    $('#new-booking').dialog('close');
    refresh_cal();
};

function make_booking() {
    var params = {};
    params.resource_id = parseInt($('#resource-select').val());
    params.resource_name = resource_map[params.resource_id];

    var start_time = new Date(new_booking_date.getTime());
    var hrs_mins = $('#new-starts').val().split(':');
    var hrs = hrs_mins[0];
    var mins = hrs_mins[1];
    start_time.setHours(hrs);
    start_time.setMinutes(mins);
    params.start_time = to_iso_datetime(start_time)

    var end_time = new Date(new_booking_date.getTime());
    var hrs_mins = $('#new-ends').val().split(':');
    var hrs = hrs_mins[0];
    var mins = hrs_mins[1];
    end_time.setHours(hrs);
    end_time.setMinutes(mins);
    params.end_time = to_iso_datetime(end_time)

    params.quantity = $('#new-quantity').val() || 1;
    params.member = $('#for-member').val();

    jsonrpc('usage.new', params, on_new_booking, error);
};

$('#new-booking-form').submit( function () {
    $(this).checkValidity();
    make_booking();
    return false;
});
