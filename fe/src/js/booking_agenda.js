function get_bookings() {
    var params = {};
    params = {start: '2011-12-01', end: '2011-12-31', res_owner_ids:[9]};
    jsonrpc('usages.find_by_date', params, on_find_usages);
};

function on_find_usages(resp) {
    var bookings = resp.result;
    render_bookings(bookings);
};

function render_bookings(bookings) {
    $('#bookings-tmpl').tmpl(bookings).appendTo('#agenda');
};

get_bookings();
