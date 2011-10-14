function login() {
    var action_status = $('#login-form .action-status');
    action_status.text("Logging in...");
    var theform = $('#login-form');
    var inputs = theform.serializeArray();
    var params = {}
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
    if(!theform.checkValidity || theform.checkValidity()){
        jsonrpc('login', params, success, error);
        return false;
    };
};

$('#login-btn').click(login);

function signup() {
    $('#signup-box').dialog({ title: "Get ready", width: 500});
};

function register() {
    var action_status = $('#signup-form .action-status');
    action_status.text("Signing up...");
    var inputs = $('#signup-form').serializeArray();
    var params = {}
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
    };
    function success(resp) {
        action_status.text("Thank you. Activation email is on the way.").addClass('status-success');
        setTimeout("$('#signup-box').dialog('close')", 3000);
    };
    function error() {
        action_status.text("Error signing up. Try again").attr('class', 'status-fail');
    };
    jsonrpc('registration.new', params, success, error);
};

$('#signup-btn').click(signup);
$('#register-btn').click(register);

function enterKey(evt) {
    var evt = (evt) ? evt : event
    var charCode = (evt.which) ? evt.which : evt.keyCode
    if (charCode == 13) {
      login();
    };
}; 

document.body.onkeypress = enterKey;
