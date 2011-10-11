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
    params['owner'] = current_bizplace;    
    params['picture'] = picture;
    function success() {
        $('#CreateResource-msg').html("<big>☑</big> Resource Created successful.");
        };
    function error() {
        $('#CreateResource-msg').html("<big>Error in Resource Creation. Try again</big>");
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
