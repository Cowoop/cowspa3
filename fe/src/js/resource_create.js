//*****************************Global Section***********************************
var picture = null;
var image_size_limit = 256000;//256kb
var checked_map = {'checked':true, 'on':true, undefined:false};
//xxxxxxxxxxxxxxxxxxxxxxxxxxxEnd Global Sectionxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

//****************************Save Resource*************************************
var create_resource_form = $('#createresource_form');
$("#time_based").click();
function create_resource () {
    var action_status = $('#createresource_form .action-status');
    action_status.text("Creating resource ...");
    var inputs = create_resource_form.serializeArray();
    var params = {}
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
    }
    params.owner = current_ctx;    
    params.picture = picture;
    params.time_based = checked_map[params.time_based];
    function success() {
        action_status.text("Resource created successfully").attr('class', 'status-success');
        setTimeout(function(){
            window.location = basepath + '/resources';
        }, 1000);
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
    if(files.length == 1){
        if(files[0].size <= image_size_limit)
            reader.readAsDataURL(files[0]);
        else
            alert("Image size exceeds image upload limit, Image size must be less than "+ (image_size_limit/1000) + "kb.");
    }
});
//xxxxxxxxxxxxxxxxxxxxxxxxxEnd Upload Invoice Picturexxxxxxxxxxxxxxxxxxxxxxxxxxx
