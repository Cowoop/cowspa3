$('#save-btn').click(function () {
    var inputs = $('#createplan_form').serializeArray();
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
    params['bizplace_id'] = $("#bizplaces").val();
    jsonrpc('plan.new', params, success, error);
});
    
$("#cancel-btn").click(function (){
    $("#createplan_form").hide();
    $("#new-plan").show();
    $("#plan_list").show();
});

$(document).ready(function() {
    var params = {}
    function success(resp) {
        var markup = "<div class='plan-box'><div class='plan-title'>${name}</div> ${description}</div>";
        $.template( "planTemplate", markup );
        no_plans = resp['result'].length;
        $.tmpl( "planTemplate", resp['result'].slice(0,no_plans/2)).appendTo( "#plan_list #left" );
        $.tmpl( "planTemplate", resp['result'].slice(no_plans/2)).appendTo( "#plan_list #right" );
        };
    function error() {
        };
    params['bizplace_id'] = $("#bizplaces").val();
    jsonrpc('bizplace_plans.list', params, success, error);
});

$("#new-plan").click(function (){
    $("#plan_list").hide();
    $("#new-plan").hide();
    $("#createplan_form #name").val("");
    $("#createplan_form #description").val("");
    $("#createplan_form").show();
});
