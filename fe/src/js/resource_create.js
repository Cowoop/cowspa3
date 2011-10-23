//*****************************Global Section***********************************
var picture = null;
//xxxxxxxxxxxxxxxxxxxxxxxxxxxEnd Global Sectionxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

//****************************Save Resource*************************************
var create_resource_form = $('#createresource_form');

function create_resource () {
    var action_status = $('#createresource_form .action-status');
    action_status.text("Creating resource ...");
    var inputs = create_resource_form.serializeArray();
    var params = {}
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
    }
    params['owner'] = current_ctx;    
    params['picture'] = picture;
    function success() {
        action_status.text("Resource created successfully").attr('class', 'status-success');
    };
    function error() {
        action_status.text("Error in creating resource").attr('class', 'status-fail');
    };
    jsonrpc('resource.new', params, success, error);
};

create_resource_form.submit( function () {
    $(this).checkValidity();
    create_resource();
    return false;
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
