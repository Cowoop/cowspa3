$('#save-btn').click(function () {
    var inputs = $('#createplan_form').serializeArray();
    var params = {}
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
        }
    function success() {
        $('#CreatePlan-msg').html("<big>☑</big> Plan Created successful.");
        };
    function error() {
        $('#CreatePlan-msg').html("<big>Error in Plan Creation. Try again</big>");
        };
    jsonrpc('plan.new', params, success, error);
    });
