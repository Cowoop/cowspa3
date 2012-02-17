if (member_name) { set_member_name(member_name); };
init_autocomplete();
init_nav();

function on_roles(roles) {}; // HOOK

// TODO : Update role_filter when additional roles like accountant are added

if(current_userid) {
    var params = {'user_id': current_userid};
    jsonrpc('roles.list', params, on_roles_list);
};
