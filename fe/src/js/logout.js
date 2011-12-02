function success(resp) {
    delete_cookie('authcookie');
    delete_cookie('roles');
    delete_cookie('user_id');
    delete_cookie('member_name');
    window.location = "/login";
};
function error() {};
params = { 'token' : $.cookie('authcookie')};
jsonrpc('logout', params, success, error);
