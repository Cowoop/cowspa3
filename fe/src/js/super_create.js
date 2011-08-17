$('#save-btn').click(function () {
    var inputs = $('#createsuper_form').serializeArray();
    var params = {}
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
        }
    function success() {
        $('#CreateSuper-msg').html("<big>☑</big> Super User Created successfully.");
        };
    function error() {
        $('#CreateSuper-msg').html("<big>Error in Super User Creation. Try again</big>");
        };
    jsonrpc('member.create_admin', params, success, error);
    });
