var tariff_baseurl =  basepath + '/tariffs/';
var tariff_id = null;
var action_status = $('#tariff_form .action-status');
var tariffs_title = $('#content-title').text();

function update_tariff(theform) {
    var inputs = theform.serializeArray();
    var params = {}
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
    }
    function success() {
        action_status.text("Tariff Updated successfully.").attr('class', 'status-success');
        setTimeout(function(){
            window.location = tariff_baseurl;
        }, 1000);
    };
    function error() {
        action_status.text("Error while Updating Tariff.").attr('class', 'status-fail');
    };
    params['owner'] = current_ctx;
    params['type'] = 'tariff';
    params['res_id'] = tariff_id;
    jsonrpc('resource.update', params, success, error);
}

$("#cancel-btn").click(function (){
    $("#tariff_form").hide();
    $("#new-tariff").show();
    $("#tariff_list").show();
    $('#content-title').text(tariffs_title);
    window.location = tariff_baseurl;
});

function show_editform(id) {
    $("#tariff_list").hide();
    $("#tariff_form").show();

    function success(resp) {
        tariff = resp['result'];
        $('#content-title').text(tariff.name);
        $('#tariff_form #name').val(tariff.name);
        $('#tariff_form #short_description').val(tariff.short_description);
    };

    function error() {
        alert('Unable to get Tariff Information');
    };

    var params = {'res_id': id};
    jsonrpc('resource.info', params, success, error);
}

function act_on_route(id) {
    if (tariff_id != id) {
        tariff_id = id;
    }
};

function setup_routing () {
    var routes = {
        '/:id': {
            '/edit': show_editform,
            on: act_on_route
        },
    };

    Router(routes).configure({ recurse: 'forward' }).init();
};

setup_routing();

$(document).ready(function() {
    var params = {}
    function success(resp) {
//        var markup = "<div class='tariff-box'><div class='tariff-title'>${name}</div> ${short_description}</div>";
//        $.template( "tariffTemplate", markup );
        no_tariffs = resp['result'].length;
        $('#tariff_tmpl').tmpl(resp['result'].slice(0,no_tariffs/2)).appendTo( "#tariff_list #left" );
        $('#tariff_tmpl').tmpl(resp['result'].slice(no_tariffs/2)).appendTo( "#tariff_list #right" );
        };
    function error() {
        };
    params['owner'] = current_ctx;
    jsonrpc('tariffs.list', params, success, error);
});

$("#new-tariff").click(function (){
    window.location = basepath + '/tariff/new'
});

$('#tariff_form').submit(function () {
    var theform = $(this);
    theform.checkValidity();
    update_tariff(theform);
    return false;
});
