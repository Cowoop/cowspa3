$('#save-btn').click(function () {
    var inputs = $('#createbizplace_form').serializeArray();
    var params = {}
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
        }
    function success() {
        $('#CreateBizplace-msg').html("<big>☑</big> Place Created Successfully.");
        };
    function error() {
        $('#CreateBizplace-msg').html("<big>Error in Place Creation. Try again</big>");
        };
    jsonrpc('bizplace.new', params, success, error);
    });
