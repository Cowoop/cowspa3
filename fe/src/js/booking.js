var day_miliseconds = 24 * 60 * 60 * 1000;
var resource_map = {};
var shown_dates = [];
var new_booking_date = null;
var dropped_slot = null;
var booking_action = 'click';

function error(resp) {
    alert('Remote error: ' + resp.error.message);
};

function add_days(adate, days) {
    return new Date(adate.getTime() + (days * day_miliseconds))
};

function set_day_titles() {
    var date_selected = get_selected_date();
    $('.day-title').each( function (idx) {
        var date_next = add_days(date_selected, (idx - 3));
        var date_text = $.datepicker.formatDate('D d', date_next)
        $(this).text(date_text);
        if (idx == 3) {
            $(this).addClass('today');
        } else {
            $(this).removeClass('today');
        };
        shown_dates[idx] = date_next;
    });
};

$('#booking-date-inp').datepicker( {
    onSelect: refresh_cal
});

function get_selected_date() {
    return new Date($('#booking-date-inp').val());
};

function on_get_usages(resp) {
    mark_slots(resp.result);
    init_cal();
};

function get_usages(resource_id) {
    var params = {'resource_ids': [resource_id],
        calc_mode: [1],
        start: to_iso_date(add_days(get_selected_date(), -3)),
        end: to_iso_date(add_days(get_selected_date(), 3))
    };
    jsonrpc("usages.find", params, on_get_usages, error);
};

function get_bookings(start, end, bizplace_id) {
    var params = { res_owner_ids: current_ctx,
        start: null, // TODO
        end: null // TODO
    };
};

function mark_slot(usage) {
    var booking_id = usage.id;
    var start_time = iso2date(usage.start_time);
    var end_time = iso2date(usage.end_time);
    for (i in shown_dates) {
        if (shown_dates[i] > start_time) {
            break;
        };
    };
    var matched_day_idx = i-1;
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
        // $(this).draggable({containment: 'window', snap: 'window'});
    });

    var this_booking_slot = 'booking_' + booking_id;
    $(matched_slots).wrapAll('<DIV id="' + this_booking_slot + '" class="booking"></DIV>');
    $('#' + this_booking_slot).draggable({appendTo: "#booking-cal", helper: "clone", cursor: 'move', containment: '.cal-week'});
};

function on_drop_booking(event, ui ) {
    booking_action = 'drop';
    var draggable = ui.draggable;
    var current_booking_id = parseInt(draggable.attr('id').split('_')[1]);
    var date_start_end = id2datetime($(this).attr('id'));
    new_booking_date = date_start_end[0]; // global
    dropped_slot = date_start_end[1];
    get_booking_info(current_booking_id);
    // TODO: we are editing not creating
};

function get_booking_info(booking_id) {
    var params = {usage_id: booking_id};
    jsonrpc('usage.info', params, on_booking_info, error);
};

function on_booking_info(resp) {
    var booking = resp.result;
    open_edit_booking_form(booking);
};

function mark_slots(usages) {
    for (i in usages) {
        mark_slot(usages[i]);
    };
    $('.slot-available').droppable({drop: on_drop_booking});
    $('.booking').click( function () {
        booking_action = 'click';
        var booking_id = parseInt($(this).attr('id').split('_')[1]);
        get_booking_info(booking_id);
    });
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

var params = {owner: current_ctx, calc_mode: 1};
jsonrpc("resources.available", params, on_available_resources, error);

set_day_titles();

function id2datetime(id) {
    var slot_no = id.split('_')[1];
    var day_no = parseInt(slot_no.split('-')[0]);
    var thedate = add_days(get_selected_date(),  (-3 + day_no));
    var start_end = slot_no.split('-')[1].split('.');
    var start = start_end[0];
    var end = start_end[1];
    return [thedate, start, end];
};

function open_booking_form(resource_name, new_booking_date, start_time, end_time) {
    $('#booking_id').val('0'); // important
    $('#new-booking-date').text($.datepicker.formatDate('D, MM d, yy', new_booking_date));
    $('#new-starts').val(start_time);
    $('#new-ends').val(end_time);
    $('#new-ends').attr('min', start_time);
    $('#new-booking').dialog({
        title: resource_name,
        close: on_close_booking_form
    });
};

function open_edit_booking_form(booking) {
    $('#for-member').val((booking.member).toString());
    $('#booking-id').val((booking.id).toString());
    $('#for-member-search').val(booking.member_name);
    $('#new-booking-date').text($.datepicker.formatDate('D, MM d, yy', new_booking_date));
    var booking_duration = (new Date(booking.end_time)) - (new Date(booking.start_time));
    var upper_slots_time = booking_duration / 2;
    if (booking_action == 'drop') {
        var dropped_slot_time = (dropped_slot.split(':')[0] * 60 * 60 * 1000) + (dropped_slot.split(':')[1] * 60 * 1000);
        if (dropped_slot_time > upper_slots_time) {
            var offset = (dropped_slot_time - upper_slots_time);
            var start_time = new Date(new_booking_date.getTime() + offset);
            var end_time = new Date(start_time.getTime() + booking_duration);
            var start_iso = date2iso(start_time, true);
            var end_iso = date2iso(end_time, true);
        } else {
            var start_iso = '00:00';
            var end_time = new Date(new_booking_date.getTime() + booking_duration);
            var end_iso = date2iso(end_time, true);
        };
    } else {
        var start_iso = date2iso(booking.start_time);
        var end_iso = date2iso(booking.end_time);
    };
    $('#new-starts').val(start_iso);
    $('#new-ends').val(end_iso);
    $('#new-ends').attr('min', start_iso);
    $('#new-booking').dialog({
        title: booking.resource_name,
        close: on_close_booking_form
    });
};

function on_select_slots(ev, ui) {
    var selected = [];
    $( ".ui-selected", this ).each( function () {
        selected.push($(this).attr('id'));
    });
    var start = selected[0];
    var end = selected.pop();
    var date_start_end = id2datetime(start);
    new_booking_date = date_start_end[0]; // global
    var start_time = date_start_end[1];
    var end_time = id2datetime(end)[2];

    var resource_name = resource_map[$('#resource-select').val()];
    open_booking_form(resource_name, new_booking_date, start_time, end_time);
};

function on_close_booking_form() {
    $('.ui-selected').removeClass('ui-selected');
};

function init_cal() {
    $(".cal-day").selectable({
        cancel: '.slot-unavailable',
        stop: on_select_slots
    });
    $('#booking-cal').removeClass('opaq');
};

function refresh_cal() {
    set_day_titles();
    $(".cal-day").selectable('destroy');
    $('.slot-unavailable').each( function () {
        $(this).removeClass('slot-unavailable');
        $(this).removeClass('slot-available');
    });
    var resource_id = parseInt($('#resource-select').val());
    if (resource_id) {
        get_usages(resource_id);
    };
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

    // params.quantity = $('#new-quantity').val() || 1;
    params.member = $('#for-member').val();

    var usage_id = $('#booking-id').val();

    if (usage_id == 0) {
        jsonrpc('usage.new', params, on_new_booking, error);
    } else {
        params.usage_id = usage_id;
        jsonrpc('usage.update', params, on_new_booking, error);
    };
};

$('#new-booking-form').submit( function () {
    $(this).checkValidity();
    make_booking();
    return false;
});
