function login() {
    var action_status = $('#login-form .action-status');
    var params = {};
    var inputs = $('#login-form').serializeArray();
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
    };
    function success(resp) {
        action_status.text("Login is successful.").attr('class', 'status-success');  
        set_cookie('authcookie', resp.result.auth_token)
        set_cookie('user_id', resp.result.id)
        set_cookie('roles', resp.result.roles)
        set_member_name(resp.result.name);
        var lang = resp.result.pref.language.split('_')[0];
        // Following is hacked temporarily till we support build for more langs
        if ($.inArray(lang, ['en','de']) == -1 ) {
            lang = 'en'; // Build for this lang not available, return English as default
        }
//        var lang = resp.result.pref.language
        window.location = "/" + lang + "/" + resp.result.pref.theme + "/dashboard";
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
      activate();
    };
}; 

document.body.onkeypress = enterKey;
