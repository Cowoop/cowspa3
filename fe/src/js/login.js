H5F.setup(document.getElementById('login_form'));

$('#login-btn').click(function () {
    var params = {'username': $('#username').val(), password: $('#password').val()};
    function success() {
        $('#login-msg').html("<big>☑</big> Login is successful.");
    };
    function error() {
        $('#login-msg').html("<big>Authentication Error. Try again</big>");
    };
    jsonrpc('login', params, success, error);
});
