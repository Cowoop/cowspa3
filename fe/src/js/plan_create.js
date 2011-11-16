$('#save-btn').click(function () {
    var inputs = $('#createtariff_form').serializeArray();
    var params = {}
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
    }
    function success() {
        $('#CreatePlan-msg').html("<big>☑</big> Tariff Created successfully.");
        setTimeout(function(){
            window.location.reload();
        }, 1000);
    };
    function error() {
        $('#CreatePlan-msg').html("<big>Error in Tariff Creation. Try again</big>");
    };
    params['owner'] = current_ctx;
    params['type'] = 'tariff';
    jsonrpc('resource.new', params, success, error);
});
    
$("#cancel-btn").click(function (){
    $("#createtariff_form").hide();
    $("#new-tariff").show();
    $("#tariff_list").show();
});

$(document).ready(function() {
    var params = {}
    function success(resp) {
        var markup = "<div class='tariff-box'><div class='tariff-title'>${name}</div> ${short_description}</div>";
        $.template( "tariffTemplate", markup );
        no_tariffs = resp['result'].length;
        $.tmpl( "tariffTemplate", resp['result'].slice(0,no_tariffs/2)).appendTo( "#tariff_list #left" );
        $.tmpl( "tariffTemplate", resp['result'].slice(no_tariffs/2)).appendTo( "#tariff_list #right" );
        };
    function error() {
        };
    params['owner'] = current_ctx;
    params['type'] = 'tariff';
    jsonrpc('resource.list', params, success, error);
});

$("#new-tariff").click(function (){
    $("#tariff_list").hide();
    $("#new-tariff").hide();
    $("#createtariff_form #name").val("");
    $("#createtariff_form #description").val("");
    $("#createtariff_form").show();
});
