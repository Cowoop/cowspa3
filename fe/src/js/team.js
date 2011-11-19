var new_member_id = null;

$('#team_form').hide();
$('#team_list').show();

$('#new-team').click(function() {
    $('#team_list').hide();
    $('#team_form').show();
});

$('.remove_staff').click(function() {
    return false;
});

function search_members_autocomplete() {
    $('input#member_name').autoSuggest("/search/members", {
        selectedItemProp: "name",
        selectedValuesProp: "id", 
        searchObjProps: "name, email, id",
        minChars: 1,
        selectionLimit: 0, 
        startText: "Search member by name, email or id",
        resultClick: function (data) {
            //TODO : Not working
           $('#member_name').val(data['attributes']['name']);
            new_member_id = data['attributes']['id'];
        } 
    });
};

function load_team() {
    function success(resp) {
        $('#team_tmpl').tmpl(resp['result']).appendTo('#team_list');
    };

    function error() {
        alert('Error getting team information');
    };

    var params = {};
    params = {'context': current_ctx}
    if(params['context']) {
        jsonrpc('roles.team', params, success, error); 
    };

}

$(document).ready(function() {
    search_members_autocomplete();
    load_team();
});


var theform = $('#team_form');

function add_roles() {
    //var inputs = theform.serializeArray();
    var action_status = $('#team_form .action-status');
    var roles = [];
    var params = {};
    $('#roles :checked').each(function() {
       roles.push($(this).val());
     });

    //for(var i in inputs){
        //params[inputs[i].name] = inputs[i].value;
    //}
    params['context'] = current_ctx
    params['user_id'] =  new_member_id
    params['roles'] =  roles

    function success() {
        action_status.text("New role(s) assigned successfully").attr('class', 'status-success');
        setTimeout(function(){
            window.location.reload()
        }, 1000);
    };
    function error() {
        action_status.text("Error assigning role(s)").attr('class', 'status-fail');
    };
    jsonrpc('roles.add', params, success, error);
};

theform.submit( function () {
    $(this).checkValidity();
    add_roles();
    return false;
});
