var theform = $('#bizplace_form');

function create_bizplace() {
    var inputs = theform.serializeArray();
    var action_status = $('#bizplace_form .action-status');
    var params = {};
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
    }
    function success() {
        action_status.text("Location created successfully").attr('class', 'status-success');
        window.location.reload();
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
