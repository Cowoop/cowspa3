function login() {
    var action_status = $('#login-form .action-status');
    var params = {};
    var inputs = $('#login-form').serializeArray();
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
    };
    function success(resp) {
        action_status.text("Login is successful.").attr('class', 'status-success');
        window.location = "/"+resp['result']['language']+"/"+resp['result']['theme']+"/dashboard";
        };
    function error() {
        action_status.text("Authentication Error. Try again").attr('class', 'status-fail');
        };
    jsonrpc('login', params, success, error);
};

function activate() {
    var action_status = $('#login-form .action-status');
    action_status.text("Activating the account ...");
    var params = {'key': window.location.hash.slice(1)}
    var inputs = $('#login-form').serializeArray();
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
    };
    function success(resp) {
        action_status.text("Account activated! Now logging in ..").attr('class', 'status-success');
        login();
        };
    function error() {
        action_status.text("Activation failed. Try different username").attr('class', 'status-fail');
        };
    jsonrpc('registration.activate', params, success, error);
};

$('#login-btn').click(activate);

function enterKey(evt) {
    var evt = (evt) ? evt : event
    var charCode = (evt.which) ? evt.which : evt.keyCode
    if (charCode == 13) {
      login();
    };
}; 

document.body.onkeypress = enterKey;
