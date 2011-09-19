function login() {
    var action_status = $('#login-form .action-status');
    action_status.text("Logging in...");
    var inputs = $('#login-form').serializeArray();
    var params = {}
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
        }
    function success(resp) {
        action_status.text("Login is successful.").attr('class', 'status-success');
        window.location = "/"+resp['result']['language']+"/"+resp['result']['theme'].toLowerCase()+"/dashboard";
        };
    function error() {
        action_status.text("Authentication Error. Try again").attr('class', 'status-fail');
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
