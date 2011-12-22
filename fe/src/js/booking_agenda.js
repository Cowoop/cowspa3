function get_bookings(start, end) {
    var params = {};
    params = {start: start, end: end, res_owner_ids:[current_ctx], calc_mode:[1]};
    jsonrpc('usages.find_by_date', params, on_find_usages);
};

function on_find_usages(resp) {
    var bookings = resp.result;
    render_bookings(bookings);
};

function render_bookings(bookings) {
    $('#pane-booking').empty();
    $('#bookings-tmpl').tmpl(bookings).appendTo('#pane-booking');
};

$('#booking-date-inp').datepicker( {
    changeMonth: true,
    changeYear: true,
    showButtonPanel: true,
    dateFormat: 'MM yy',
    onSelect: function(dateText, ui) { 
        var selected = new Date(ui.selectedYear, ui.selectedMonth, ui.selectedDay);
        var week_start_end = get_week_range(selected);
        get_bookings(week_start_end[0], week_start_end[1]);
    }
});
