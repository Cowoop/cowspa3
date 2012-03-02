var day_miliseconds = 24 * 60 * 60 * 1000;
var resource_map = {};
var shown_dates = [];
var new_booking_date = null;
var dropped_slot = null;
var booking_action = 'click';

function add_days(adate, days) {
    return new Date(adate.getTime() + (days * day_miliseconds));
};

function set_day_titles() {
    var date_selected = get_selected_date();
    $('.day-title').each( function (idx) {
        var date_next = add_days(date_selected, (idx - 3));
        // var date_text = $.datepicker.formatDate('D d', date_next)
        var date_text = moment(date_next).format("MMM D");
        $(this).text(date_text);
        if (idx == 3) {
            $(this).addClass('today');
        } else {
            $(this).removeClass('today');
        };
        shown_dates[idx] = date_next;
    });
};

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
        start: date2isodate(add_days(get_selected_date(), -3)),
        end: date2isodate(add_days(get_selected_date(), 3))
    };
    jsonrpc("usages.find", params, on_get_usages);
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
    for (var i=0; i < shown_dates.length; i++) {
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
    if (($.inArray(current_role, ['host', 'director', 'admin']) != -1) || ((current_role == 'member') && (usage.member_id == current_userid))) {
        var this_slot = $('#' + this_booking_slot)
        this_slot.draggable({appendTo: "#booking-cal", helper: "clone", cursor: 'move', containment: '.cal-week'});
        this_slot.addClass('booking-editable');
    };
};

function on_drop_booking(event, ui ) {
    booking_action = 'drop';
    var draggable = ui.draggable;
    var current_booking_id = parseInt(draggable.attr('id').split('_')[1], 10);
    var date_start_end = id2datetime($(this).attr('id'));
    new_booking_date = date_start_end[0]; // global
    dropped_slot = date_start_end[1];
    get_booking_info(current_booking_id);
    // TODO: we are editing not creating
};

function get_booking_info(booking_id) {
    var params = {usage_id: booking_id};
    jsonrpc('usage.details', params, on_booking_info, error);
};

function on_booking_info(resp) {
    var booking = resp.result;
    open_edit_booking_form(booking);
};

function mark_slots(usages) {
    for (var i=0; i < usages.length; i++) {
        mark_slot(usages[i]);
    };
    $('.slot-available').droppable({drop: on_drop_booking});
    $('.booking-editable').click( function () {
        booking_action = 'click';
        var booking_id = parseInt($(this).attr('id').split('_')[1], 10);
        get_booking_info(booking_id);
    });
};

function on_available_resources(resp) {
    var resources = resp.result;
    $('#resource-opt').tmpl(resources).appendTo('#resource-select');
    for (var i=0; i < resources.length; i++) {
        resource = resources[i];
        resource_map[resource.id] = resource;
    };
};

function id2datetime(id) {
    var slot_no = id.split('_')[1];
    var day_no = parseInt(slot_no.split('-')[0], 10);
    var thedate = add_days(get_selected_date(),  (-3 + day_no));
    var start_end = slot_no.split('-')[1].split('.');
    var start = start_end[0];
    var end = start_end[1];
    return [thedate, start, end];
};

function open_booking_form(resource_id, resource_name, new_booking_date, start_time, end_time) {
    $('#booking-id').val('0'); // important
    $('#new-booking-form').reset();
    // $('#new-booking-date').text($.datepicker.formatDate('D, MM d, yy', new_booking_date));
    $('#new-booking-date').text(moment(new_booking_date).format("ddd, MMMM Do, YYYY"));
    $('#new-starts').val(start_time);
    $('#new-ends').val(end_time);
    $('#new-ends').attr('min', start_time);
    // $('#contained-usages-tmpl').tmpl(resource_map[resource_id]['contained']).appendTo('#contained-usages')
    $('#new-booking').dialog({
        title: resource_name,
        close: on_close_booking_form,
        width: 'auto'
    });
};

function open_edit_booking_form(booking) {
    new_booking_date = new_booking_date || iso2date(booking.start_time);
    $('#booking-name').val(booking.name);
    $('#booking-notes').val(booking.notes);
    $('#booking-no_of_people').val(booking.no_of_people);
    $('#for-member').val((booking.member).toString());
    $('#booking-id').val((booking.id).toString());
    $('#for-member-search').val(booking.member_name);
    // $('#new-booking-date').text($.datepicker.formatDate('D, MM d, yy', (new_booking_date)));
    $('#new-booking-date').text(moment(new_booking_date).format("ddd, MMMM Do, YYYY"));
    var booking_duration = (new Date(booking.end_time)) - (new Date(booking.start_time));
    var min15 = 15*60*1000;
    var upper_slots_time = (Math.round((booking_duration / 2)/min15) * min15) - min15;
    if (booking_action == 'drop') {
        var dropped_slot_time = (dropped_slot.split(':')[0] * 60 * 60 * 1000) + (dropped_slot.split(':')[1] * 60 * 1000);
        if (dropped_slot_time > upper_slots_time) {
            var offset = (dropped_slot_time - upper_slots_time);
            var start_time = new Date(new_booking_date.getTime() + offset);
            var end_time = new Date(start_time.getTime() + booking_duration);
            var start_iso = date2isotime(start_time, true);
            var end_iso = date2isotime(end_time, true);
        } else {
            var start_iso = '00:00';
            var end_time = new Date(new_booking_date.getTime() + booking_duration);
            var end_iso = date2isotime(end_time, true);
        };
    } else {
        var start_iso = date2isotime(iso2date(booking.start_time), true);
        var end_iso = date2isotime(iso2date(booking.end_time), true);
    };
    $('#new-starts').val(start_iso);
    $('#new-ends').val(end_iso);
    $('#new-ends').attr('min', start_iso);
    for (var i=0; i< booking.usages_suggested.length; i++) {
        var usage = booking.usages_suggested[i];
        var ele = $('#resource-'+usage.resource_id);
        if (ele[0].type == 'text') {
            ele[0].value = usage.quantity;
        } else {
            ele.attr('checked', 'checked');
        };
    };
    $('#new-booking').dialog({
        title: booking.resource_name,
        close: on_close_booking_form,
        width: 'auto'
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

    var resource_id = $('#resource-select').val();
    var resource_name = resource_map[resource_id].name;
    open_booking_form(resource_id, resource_name, new_booking_date, start_time, end_time);
};

function on_close_booking_form() {
    $('.ui-selected').removeClass('ui-selected');
    new_booking_date = null;
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
    var resource_id = parseInt($('#resource-select').val(), 10);
    if (resource_id) {
        get_usages(resource_id);
    };
};

if ($('#for-member-search')[0]) {
    $('#for-member-search').autocomplete({
        source: "/search/member",
        select: function(event, ui) {
            $('#for-member').val(ui.item.id);
        }
    });
};

function on_new_booking(resp) {
    $('#new-booking').dialog('close');
    refresh_cal();
};

function make_booking() {
    
    var params = {};

    params.name = $('#booking-name').val();
    params.notes = $('#booking-notes').val();
    params.no_of_people = $('#booking-no_of_people').val();
    params.resource_owner = current_ctx;
    params.resource_id = parseInt($('#resource-select').val(), 10);
    params.resource_name = resource_map[params.resource_id].name;

    var start_time = new Date(new_booking_date.getTime());
    var hrs_mins = $('#new-starts').val().split(':');
    var hrs = hrs_mins[0];
    var mins = hrs_mins[1];
    start_time.setHours(hrs);
    start_time.setMinutes(mins);
    params.start_time = date2iso(start_time)

    var end_time = new Date(new_booking_date.getTime());
    var hrs_mins = $('#new-ends').val().split(':');
    var hrs = hrs_mins[0];
    var mins = hrs_mins[1];
    end_time.setHours(hrs);
    end_time.setMinutes(mins);
    params.end_time = date2iso(end_time)

    // params.quantity = $('#new-quantity').val() || 1;
    if ($('#for-member')[0]) {
        params.member = $('#for-member').val();
    } else {
        params.member = current_userid;
    };

    params.usages = [];
    var suggested_resources = resource_map[params.resource_id].suggested;
    for (var i=0; i<suggested_resources.length; i++) {
        var this_res = suggested_resources[i];
        var ele = $('#resource-'+this_res.id)[0];
        var quantity = 0;
        if (this_res.calc_mode == 0) {
            quantity = parseInt(ele.value, 10);
        } else {
            if (ele.checked) { quantity = 1; };
        };
        if (quantity>0) {
            params.usages.push({resource_id: this_res.id, quantity: quantity});
        };

    };

    var usage_id = $('#booking-id').val();

    if (usage_id == 0) {
        jsonrpc('usage.new', params, on_new_booking);
    } else {
        params.usage_id = usage_id;
        jsonrpc('usage.update', params, on_new_booking);
    };
};

// init

$('#booking-date-inp').datepicker( {
    onSelect: refresh_cal
});

$('#resource-select').change( function () {
    refresh_cal();
    var resource_id = $('#resource-select').val();
    $('#suggested-usages').empty();
    $('#suggested-usages-tmpl').tmpl(resource_map[resource_id]['suggested']).appendTo('#suggested-usages')
});

var params = {owner: current_ctx, for_member: current_userid};
jsonrpc("resources.available_for_booking", params, on_available_resources);

set_day_titles();

$('#new-booking-form').submit( function () {
    $(this).checkValidity();
    make_booking();
    return false;
});
