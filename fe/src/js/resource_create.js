//*****************************Global Section***********************************
var picture = null;
//xxxxxxxxxxxxxxxxxxxxxxxxxxxEnd Global Sectionxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

//****************************Save Resource*************************************
$('#save-btn').click(function () {
    var inputs = $('#createresource_form').serializeArray();
    var params = {}
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
    }
    params['owner'] = current_ctx;    
    params['picture'] = picture;
    function success() {
        $('#createresource_form .action-status').text("Resource created successfully").attr('class', 'status-success');
    };
    function error() {
        $('#createresource_form .action-status').text("Error in creating resource").attr('class', 'status-fail');
    };
    jsonrpc('resource.new', params, success, error);
});
//xxxxxxxxxxxxxxxxxxxxxxxxxxxEnd Save Resourcexxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

//***************************Upload Resource Picture****************************
$('#picture').change(function handleFileSelect(evt) {
    var files = evt.target.files;
    var reader = new FileReader();
    reader.onload = (function(e) {
        picture = e.target.result;
    });
    if(files.length == 1)
        reader.readAsDataURL(files[0]);
});
//xxxxxxxxxxxxxxxxxxxxxxxxxEnd Upload Invoice Picturexxxxxxxxxxxxxxxxxxxxxxxxxxx
