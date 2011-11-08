// Hide the form to beginwith
$('#bizplace_form').hide();
$('#location_view_form').hide();

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

function show_list() {
    $('#bizplace_form').hide();
    $('#location-list').show();
    $('#location_view_form').hide();
}

$('#bizplace_form #cancel-btn').click(show_list);
// $('#location_view_form #cancel-btn').click(show_list);

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

    $('#location_view_form #name').text(loc.name);
    $('#location_view_form #currency').text(loc.currency);
    $('#location_view_form #address').text(loc.address);
    $('#location_view_form #city').text(loc.city);
    $('#location_view_form #email').text(loc.email);
    $('#location_view_form #short_description').text(loc.short_description);
    $('#location_view_form #country').text(loc.country);

    $('input[name="name"]').val(loc.name);
    $('input[name="address"]').val(loc.address);
    $('#country option:contains("' +loc.country+ '")').attr('selected','selected');
    $('textarea[name="short_description"]').val(loc.short_description);
    $('input[name="city"]').val(loc.city);
    $('input[name="email"]').val(loc.email);
    $('#currency').val(loc.currency);
}

function bizplace_info_error() {
    alert('Error in bizplace.info')
}
function act_on_route(id) {
    $('#location-list').hide();
    $('#bizplace_form').hide();
    $('#location_view_form').show();

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

    Router(routes).use({ recurse: 'forward' }).init();
};

setup_routing();

$(document).ready(function() {
    var params = {};
    
    function success(resp) {
        $('#loc_tmpl').tmpl(resp['result']).appendTo('#location-list');
		// $('.location-title').click(function() {
  //           alert(this.id);
  //     //       $('#location-list').hide();          
  //     //       // Need to call bizplace.info and populate the view form
		//     // $('#location_view_form').show();
		// });        
    };

    function error() {
    };

    params = {'owner':$.cookie('user_id')};
    jsonrpc('bizplace.list', params, success, error);
});