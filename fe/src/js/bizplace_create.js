var theform = $('#bizplace_form');
var checked_map = {'checked':true, 'on':true, undefined:false};

function create_bizplace() {
    var inputs = theform.serializeArray();
    var action_status = $('#bizplace_form .action-status');
    var params = {};
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
    }
    params['tax_included'] = checked_map[$("#tax_included:checked").val()];
    function success() {
        action_status.text("Location created successfully").attr('class', 'status-success');
        window.location = basepath + '/dashboard';
    };
    function error() {
        action_status.text("Error in creating location").attr('class', 'status-fail');
    };
    jsonrpc('bizplace.new', params, success, error);
};

theform.submit( function () {
    $(this).checkValidity();
    create_bizplace();
    return false;
});
