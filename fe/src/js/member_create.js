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
