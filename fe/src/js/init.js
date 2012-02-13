if (member_name) { set_member_name(member_name); };
init_autocomplete();
init_nav();

function on_roles(roles) {}; // HOOK

// TODO : Update role_filter when additional roles like accountant are added

params = {'user_id':$.cookie('user_id')};
if(params['user_id']) {
    function error() {};
    jsonrpc('roles.list', params, on_roles_list, error);
};
