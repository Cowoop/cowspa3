$('#save-btn').click(function () {
    var inputs = $('#createmember_form').serializeArray();
    var params = {}
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
        }
    function success() {
        $('#CreateMember-msg').html("<big>☑</big> Member Created successful.");
        }
    function error() {
        $('#CreateMember-msg').html("<big>Error in Member Creation. Try again</big>");
        }
    jsonrpc('member.new', params, success, error);
    });
