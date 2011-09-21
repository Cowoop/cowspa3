$("#edit-link").click(function(){
    $("#preferences_view_form").hide();
    $("#preferences_edit_form").show();
});

$("#cancel-btn").click(function(){
    $("#preferences_view_form").show();
    $("#preferences_edit_form").hide();
});

//**********************Update Invoice Preference Info**************************
var logo;
$("#save-btn").click(function(){
    var params = {'owner':current_bizplace, 'logo':logo};
    var inputs = $("#preferences_edit_form").serializeArray();
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
        $("#preferences_view_form #"+inputs[i].name).text(inputs[i].value);
    }    
    $("#preferences_view_form").show();
    function success(response) {
        for(var key in response){    
            $("#preferences_view_form #"+key).text(response['result'][key]); 
            $("#preferences_edit_form #"+key).val(response['result'][key]);
        };
        $("#preferences_view_form #logo").attr('src', logo);
    };
    function error(){};    
    jsonrpc('invoicepref.update', params, success, error);
    $("#preferences_edit_form").hide();
});
//xxxxxxxxxxxxxxxxxxxxxEnd Update Invoice Preference Infoxxxxxxxxxxxxxxxxxxxxxxx

//***************************Upload Invoice Logo********************************
$('#preferences_edit_form #logo').change(function handleFileSelect(evt) {
    var files = evt.target.files;
    var reader = new FileReader();
    reader.onload = (function(e) {
        logo = e.target.result;
    });
    reader.readAsDataURL(files[0]);
});
//xxxxxxxxxxxxxxxxxxxxxxxxxxxxUpload Invoice Logoxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

//*************************Get Invoice Preference Info**************************
function success(response) {
    logo = response['result']['logo'];
    $("#preferences_view_form #logo").attr('src', logo);
    delete(response['result']['logo']);
    for(var key in response['result']){    
        $("#preferences_view_form #"+key).text(response['result'][key]); 
        $("#preferences_edit_form #"+key).val(response['result'][key]);
    };    
};
function error(){};
var params = { 'owner' : current_bizplace};
jsonrpc('invoicepref.info', params, success, error);
//xxxxxxxxxxxxxxxxxxxxxxxxEnd Get Invoice Preference Infoxxxxxxxxxxxxxxxxxxxxxxx

