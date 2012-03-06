var new_member_id = null;

$('#team_form').hide();
$('#team_list').show();

$('#new-team').click(function() {
    $('#team_list').hide();
    $('#team_form').show();
});


function search_members_autocomplete() {
    $('input#member_name').autoSuggest("/search/member", {
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

// We need to initiate appropriate states for the checkboxes
// Based on the roles
function init_checkboxes(result) {
    for (var i=0; i < result.length; i++) {
        var usrid = result[i]['user_id'];
        $('#chkboxes-'+usrid+' [name="roles"]').each(function() {
            if (result[i]['roles'].indexOf($(this).val()) != -1) {
                $(this).attr('checked', true);
            }
        });
    }
}

function load_team() {
    function success(resp) {
        $('#team_list').empty();
        $('#team_tmpl').tmpl(resp['result']).appendTo('#team_list');
        init_checkboxes(resp['result']);
        $(".remove_staff").click(function() {
            //TODO : Implement jQuery modal dialog box
            //Reference : stackoverflow.com/questions/887029/how-to-implement-confirmation-dialog-in-jquery-ui-dialog
            if (confirm("Remove member from Team?")) {
                user_id_to_remove = this.id.split('-')[1];
                remove_from_team();
            };
            return false;
        });
        $(".update_staff").click(update_roles);
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
    var action_status = $('#team_form .action-status');
    var roles = [];
    var params = {};
    $('#roles :checked').each(function() {
       roles.push($(this).val());
     });

    params['context'] = current_ctx
    params['user_id'] =  new_member_id
    params['roles'] =  roles

    function success() {
        var action_status = $('#team_form .action-status');
        action_status.text("New role(s) assigned successfully").attr('class', 'status-success');
        load_team();
        $('#team_form').hide();
        $('#team_list').show();
    };
    function error() {
        var action_status = $('#team_form .action-status');
        action_status.text("Error assigning role(s)").attr('class', 'status-fail');
    };
    jsonrpc('roles.add', params, success, error);
};

function update_roles() {
    var action_status = $('#team_form .action-status');
    var member_id = this.id.split('-')[1];
    var action_status = $('#roles-'+member_id+' .action-status');
    var roles = [];
    var params = {};
    $('#roles-'+member_id+' :checked').each(function() {
       roles.push($(this).val());
     });

    params['context'] = current_ctx
    params['user_id'] =  member_id
    params['roles'] =  roles

    function success() {
        action_status.text("New role(s) assigned successfully").attr('class', 'status-success');
        load_team();
    };
    function error() {
        var action_status = $('#team_form .action-status');
        action_status.text("Error assigning role(s)").attr('class', 'status-fail');
    };

    if(roles.length > 0) {
        jsonrpc('roles.add', params, success, error);
    } else {
        alert('Please select at least one role');
    }
};

function remove_from_team() {
    var params = {};

    params['context'] = current_ctx
    params['user_id'] = user_id_to_remove

    function success() {
        var action_status = $('#team_form .action-status');
        action_status.text("Member successfully removed from team").attr('class', 'status-success');
        load_team();
    };
    function error() {
        var action_status = $('#team_form .action-status');
        action_status.text("Error removing team member").attr('class', 'status-fail');
    };
    jsonrpc('roles.remove', params, success, error);
};


theform.submit( function () {
    $(this).checkValidity();
    add_roles();
    return false;
});

