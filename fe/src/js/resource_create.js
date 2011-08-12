H5F.setup(document.getElementById('createresource_form'));
$('#save-btn').click(function () {
    var inputs = $('#createresource_form').serializeArray();
    var params = {}
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
        }
    function success() {
        $('#CreateResource-msg').html("<big>☑</big> Resource Created successful.");
        };
    function error() {
        $('#CreateResource-msg').html("<big>Error in Resource Creation. Try again</big>");
        };
    jsonrpc('resource.new', params, success, error);
    });
