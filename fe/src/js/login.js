var ordered_roles = ['admin', 'director', 'host', 'member', 'new']
var login_form = $('#login-form');
var signup_form = $('#signup-form');

function construct_nextpage(result) {
    var lang = result.pref.language.split('_')[0];
    var role = '';
    if (result.length == 0) {
        role = 'new';
    } else {
        if (current_ctx==null) {
            current_ctx = result.roles[0].context;
            role = result.roles[0].roles[0].role;
        } else {
            var context_matched = false;
            for (idx in result.roles) {
                if (result.roles[idx].context === current_ctx) {
                    role = result.roles[idx].roles[0].role;
                    context_matched = true;
                    break;
                };
            };
            if(!context_matched) {
                current_ctx = result.roles[0].context;
                role = result.roles[0].roles[0].role;
            };
        };
    };
    return "/" + lang + "/" + role + "/" + result.pref.theme + "/dashboard";
};

function login() {
    var action_status = $('#login-form .action-status');
    var inputs = login_form.serializeArray();
    var params = {}
    for(var i in inputs) {
        params[inputs[i].name] = inputs[i].value;
    };
    function success(resp) {
        action_status.text("Login is successful.").attr('class', 'status-success');
        set_cookie('authcookie', resp.result.auth_token)
        set_cookie('user_id', resp.result.id)
        set_cookie('roles', resp.result.roles)
        set_member_name(resp.result.name);
        var nextpage = construct_nextpage(resp.result);
        window.location = nextpage;
    };
    function error() {
        action_status.text("Authentication Error. Try again").attr('class', 'status-fail');
    };
    action_status.text("Logging in...");
    jsonrpc('login', params, success, error);
};

function signup() {
    signup_form.dialog({ title: "Get ready", width: 500, height: 350});
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
