function success(resp) {
    $.cookie('authcookie', null);
    $.cookie('roles', null);
    $.cookie('user_id', null);
    $.cookie('member_name', null);
    window.location = "/login";
};
function error() {};
params = { 'token' : $.cookie('authcookie')};
jsonrpc('logout', params, success, error);
