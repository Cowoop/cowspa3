// Hide the form to beginwith
$('#bizplace_form').hide();
$('#location_view_form').hide();
$('#all_location_view').hide();

// This should be handled via show_editform() below
// href for edit link needs to be fixed and then 
// Uncomment entry in setup_routing
// Till then, following workaround
$('#location_view_form #edit-link').click(function(){
    $('#bizplace_form').show();
    $('#location_view_form').hide();
    return false;
  });

// function show_editform(id) {
//     $('#bizplace_form').show();
//     alert('Show Edit : ' + id);
// }

function show_mylocations() {
    $('#bizplace_form').hide();
    $('#my_loc_list').show();
    $('#location_view_form').hide();
    // TODO : Set the URL to ../bizplaces
}

function show_all_locations() {
    $('#bizplace_form').hide();
    $('#all_loc_list').show();
    $('#all_location_view').hide();
    // TODO : Set the URL to ../bizplaces
}

$('#bizplace_form #cancel-btn').click(show_mylocations);
$('#location_view_form #cancel-link').click(show_mylocations);
$('#all_location_view #cancel-link').click(show_all_locations);

function edit_location(theform) {
    // var loc_id = window.location.split('#').slice(1,1);
    // alert(window.loc.id);
    var inputs = theform.serializeArray();
    var action_status = $('#bizplace_form .action-status');
    var params = {'bizplace_id': loc.id}
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
    }
    function success() {
        action_status.text("Location updated successfully").attr('class', 'status-success');
    };
    function error() {
        action_status.text("Error in updating location").attr('class', 'status-fail');
    };
    jsonrpc('bizplace.update', params, success, error);
};

$('#bizplace_form').submit(function () {
    var theform = $(this);
    theform.checkValidity();
    edit_location(theform);
    return false;
});

function location_info(resp) {
    loc = resp['result'];

    // Not all fields from result are show on UI, so we get some error
    // for (var attr in loc) {
    //     $('input[name="location_'+ attr + 'name"]').val(loc.attr);    
    // }

    // for (var attrib in ['name', 'address', 'city', 'email', 'short_description', 'country']) {
    //     $('#location_view_form #location_'+attrib).text(loc.name);
    // }

    // TODO : Populate only appropriate view/form based on which tab is
    // selected

    selected_tab = $('#location_tabs').tabs('option', 'selected');

    if (selected_tab == 0) {  // My Location
        $('#location_view_form #name').text(loc.name);
        $('#location_view_form #currency').text(loc.currency);
        $('#location_view_form #address').text(loc.address);
        $('#location_view_form #city').text(loc.city);
        $('#location_view_form #email').text(loc.email);
        $('#location_view_form #short_description').text(loc.short_description);
        $('#location_view_form #country').text(loc.country);
        $('#location_view_form #phone').text(loc.phone);
        $('#location_view_form #fax').text(loc.fax);
        $('#location_view_form #host_email').text(loc.host_email);
        $('#location_view_form #booking_email').text(loc.booking_email);

        $('input[name="name"]').val(loc.name);
        $('input[name="address"]').val(loc.address);
        $('#country option:contains("' +loc.country+ '")').attr('selected','selected');
        $('textarea[name="short_description"]').val(loc.short_description);
        $('input[name="city"]').val(loc.city);
        $('input[name="email"]').val(loc.email);
        $('#currency').val(loc.currency);
        $('input[name="email"]').val(loc.email);
        $('input[name="host_email"]').val(loc.host_email);
        $('input[name="booking_email"]').val(loc.booking_email);
        $('input[name="phone"]').val(loc.phone);
        $('input[name="fax"]').val(loc.fax);

        $('#location_view_form').show();
        $('#my_loc_list').hide();
        $('#bizplace_form').hide();
    } else {
        $('#all_location_view #name').text(loc.name);
        $('#all_location_view #currency').text(loc.currency);
        $('#all_location_view #address').text(loc.address);
        $('#all_location_view #city').text(loc.city);
        $('#all_location_view #email').text(loc.email);
        $('#all_location_view #short_description').text(loc.short_description);
        $('#all_location_view #country').text(loc.country);
        $('#all_location_view #phone').text(loc.phone);
        $('#all_location_view #fax').text(loc.fax);
        $('#all_location_view #host_email').text(loc.host_email);
        $('#all_location_view #booking_email').text(loc.booking_email);
        $('#all_location_view').show();
        $('#all_loc_list').hide();
    }
}

function bizplace_info_error() {
    alert('Error in bizplace.info')
}

function act_on_route(id) {
    var params = {'bizplace_id': id};
    jsonrpc('bizplace.info', params, location_info, bizplace_info_error);
};

function setup_routing () {
    var routes = {
        '/:id': {
            // '/edit': show_editform,
            on: act_on_route
        },
    };

    Router(routes).configure({ recurse: 'forward' }).init();
};

setup_routing();

$(document).ready(function() {
    $('#location_tabs').tabs({
        collapsible:false
    });
    load_my_locations();
    load_all_locations();
});

function load_my_locations() {
    function success(resp) {
        $('#my_loc_tmpl').tmpl(resp['result']).appendTo('#my_loc_list');
    };

    function error() {
        alert('Error getting my locations');
    };

    var params = {};
    params = {'user_id': current_userid}
    if(params['user_id']) {
        jsonrpc('roles.list', params, success, error); 
    };

};

function load_all_locations() {
    function success(resp) {
        $('#all_loc_tmpl').tmpl(resp['result']).appendTo('#all_loc_list');
    };

    function error() {
        alert('Error getting all locations');
    };

    var params = {};
    jsonrpc('bizplace.all', params, success, error);
};
