$('#createmember_form').submit(function () {
    var theform = $(this);
    theform.checkValidity();
    var inputs = theform.serializeArray();
    var params = {};
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
    };
    function success() {
        $('.action-status').text("Member Created successfully.").addClass('status-success');
    };
    function error() {
        $('.action-status').text("Error in Member Creation").addClass('status-fail');
    };
    $('.action-status').text("").removeClass('status-fail status-success');
    jsonrpc('member.new', params, success, error);
    return false
});

function register() {
    var action_status = $('#signup-form .action-status');
    var inputs = $('#signup-form').serializeArray();
    var params = {}
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
    };
    function success(resp) {
        action_status.text("Thank you. Activation email is on the way.").addClass('status-success');
        setTimeout("$('#signup-box').dialog('close')", 3000);
    };
    function error() {
        action_status.text("Error signing up. Try again").attr('class', 'status-fail');
    };
    jsonrpc('registration.invite', params, success, error);
    action_status.text("Sending invitation...");
};

$('#signup-form').submit(function () {
    $(this).checkValidity();
    register();
    return false;
});

$('.sidebar').show();

$('#invite-btn').click( function () {
    $('#invite').dialog({
        title: "Invitation form"
    });
});
