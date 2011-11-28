function sevendays(adate) {
    var days = [];
    for (var i=0;  i<= 6; i++) {
        days[i] = new Date(adate.getTime() + (24 * 60 * 60 * 1000));
    };
    return days;
};

function set_day_titles() {
    var date_selected = new Date($('#booking-date-inp').val());
    $('.day-title').each( function (idx) {
        var date_next = new Date(date_selected.getTime() + ((idx - 3) * 24 * 60 * 60 * 1000));
        var date_text = $.datepicker.formatDate('D d', date_next)
        $(this).text(date_text);
    });
};

function error(resp) {
    alert('Remote error: ' + resp.result.message);
};

function on_available_resources(resp) {
    tariffs = resp.result;
    $('#resource-opt').tmpl(tariffs).appendTo('#resource-select');
};

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
