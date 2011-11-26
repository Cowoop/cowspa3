$('#booking-date-inp-vis').datepicker( {
    altFormat: 'yy-mm-dd',
    altField: '#booking-date-inp',
    dateFormat: 'M d, yy'
});

function init_cal() {
    $(".cal-day").selectable({
        selected: function () {  }
    });
};

$('#booking-date-inp').change ( function () {
    alert(1);
});
