var login_form = $('#login-form');
var signup_form = $('#signup-form');

function login() {
    var action_status = $('#login-form .action-status');
    var inputs = login_form.serializeArray();
    var params = {}
    for(var i in inputs) {
        params[inputs[i].name] = inputs[i].value;
    };
    function success(resp) {
        action_status.text("Login is successful.").attr('class', 'status-success');
        window.location = "/"+resp['result']['language']+"/"+resp['result']['theme']+"/dashboard";
    };
    function error() {
        action_status.text("Authentication Error. Try again").attr('class', 'status-fail');
    };
    action_status.text("Logging in...");
    jsonrpc('login', params, success, error);
};

function signup() {
    signup_form.dialog({ title: "Get ready", width: 500});
};

function register() {
    var action_status = $('#signup-form .action-status');
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
    action_status.text("Signing up...");
};

login_form.submit(function () {
    $(this).checkValidity();
    login();
    return false;
});

signup_form.submit(function () {
    $(this).checkValidity();
    register();
    return false;
});

$('#signup-btn').click(signup);

function enterKey(evt) {
    var evt = (evt) ? evt : event
    var charCode = (evt.which) ? evt.which : evt.keyCode
    if (charCode == 13) {
      login();
    };
}; 

document.body.onkeypress = enterKey;
