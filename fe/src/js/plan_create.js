var tariff_baseurl =  basepath + '/tariffs/';
var tariff_id = null;
var action_status = $('#tariff_form .action-status');

function create_tariff() {
    var inputs = $('#tariff_form').serializeArray();
    var params = {}
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
    }
    function success() {
        action_status.text("Tariff Created successfully.").attr('class', 'status-success');
        setTimeout(function(){
            window.location = tariff_baseurl;
        }, 1000);
    };
    function error() {
        action_status.text("Error in Tariff Creation.").attr('class', 'status-fail');
    };
    params['owner'] = current_ctx;
    params['type'] = 'tariff';
    jsonrpc('resource.new', params, success, error);
}

$("#cancel-btn").click(function (){
    $("#tariff_form").hide();
    window.location = tariff_baseurl;
});

$(document).ready(function() {
    $("#tariff_form #name").val("");
    $("#tariff_form #short_description").val("");
    $("#tariff_form #default_price").val("");
    $("#tariff_form [for='default_price']").text($("#tariff_form [for='default_price']").text() + ' (' + locale_data.currency_symbol + ')')
    $("#tariff_form").show();
});

$('#tariff_form').submit(function () {
    var theform = $(this);
    theform.checkValidity();
    create_tariff();
    return false;
});
