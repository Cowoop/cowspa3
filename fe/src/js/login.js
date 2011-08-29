function login() {
    $('#login-msg').html("Logging in...");
    var inputs = $('#login_form').serializeArray();
    var params = {}
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
        }
    function success(resp) {
        // console.log(resp);
        $('#login-msg').html("<big>☑</big> Login is successful.");
        window.location = "/en/default/dashboard"
        };
    function error() {
        $('#login-msg').html("<big>Authentication Error. Try again</big>");
        };
    jsonrpc('login', params, success, error);
};

$('#login-btn').click(login);

function enterKey(evt) {
    var evt = (evt) ? evt : event
    var charCode = (evt.which) ? evt.which : evt.keyCode
    if (charCode == 13) {
      login();
    };
}; 

document.body.onkeypress = enterKey;
