H5F.setup(document.getElementById('login_form'));
$('#login-btn').click(function () {
    var inputs = $('#login_form').serializeArray();
    var params = {}
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
        }
    function success() {
        $('#login-msg').html("<big>☑</big> Login is successful.");
        };
    function error() {
        $('#login-msg').html("<big>Authentication Error. Try again</big>");
        };
    jsonrpc('login', params, success, error);
    });
