//****************************Global Section************************************
var invoice_pref_info;
var changed_values = {};
//xxxxxxxxxxxxxxxxxxxxxxxxxxEnd Global Sectionxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

$("#edit-link").click(function(){
    $("#view-section").hide();
    $("#edit-section").show();
});

$("#cancel-btn").click(function(){
    $("#edit-section").hide();
    $("#email_text").val(invoice_pref_info['email_text']);
    $("#terms_and_conditions").val(invoice_pref_info['terms_and_conditions']);
    $("#due_date").val(invoice_pref_info['due_date']);
    $("#bank_details").val(invoice_pref_info['bank_details']);
    $("#bcc_invoice").val(invoice_pref_info['bcc_email']);
    changed_values = {}; 
    $('#edit_invoicepref-msg').html("");
    $("#view-section").show();
});

//**********************Update Invoice Preference Info**************************
$("#save-btn").click(function(){
    var params = {'owner':current_ctx};
    for(var key in changed_values){
        if(changed_values[key]==invoice_pref_info[key]){
            delete(changed_values[key])
        }
    }    
    function success() {
        if('logo' in changed_values){
            $("#data-logo").attr('src', changed_values['logo']);
            invoice_pref_info['logo'] = changed_values['logo'];
            delete(changed_values['logo']);
        }
        for(key in changed_values){
            $("#data-"+key).text(changed_values[key]);
            invoice_pref_info[key] = changed_values[key];
        }
        changed_values = {};
        $('#edit_invoicepref-msg').html("");
        $("#edit-section").hide();
        $("#view-section").show();
    };
    function error(){
        $('#edit_invoicepref-msg').html("<big>Error in Updating Invoice Preferences. Try again</big>");
    };
    if($.isEmptyObject(changed_values) == false){    
        changed_values['owner'] = current_ctx; 
        jsonrpc('invoicepref.update', changed_values, success, error);
    }
    else{
        $('#edit_invoicepref-msg').html("");
        $("#edit-section").hide();
        $("#view-section").show();
    }
});
//xxxxxxxxxxxxxxxxxxxxxEnd Update Invoice Preference Infoxxxxxxxxxxxxxxxxxxxxxxx

//***************************Upload Invoice Logo********************************
$('#logo').change(function handleFileSelect(evt) {
    var files = evt.target.files;
    var reader = new FileReader();
    reader.onload = (function(e) {
        changed_values['logo'] = e.target.result;
    });
    if(files.length == 1)
        reader.readAsDataURL(files[0]);
});
//xxxxxxxxxxxxxxxxxxxxxxxxxEnd Upload Invoice Logoxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

//*************************Get Invoice Preference Info**************************
function success(response) {
    invoice_pref_info = response['result'];
    $("#data-logo").attr('src', response['result']['logo']);
    $("#data-email_text").text(response['result']['email_text']); 
    $("#email_text").val(response['result']['email_text']);
    $("#data-terms_and_conditions").text(response['result']['terms_and_conditions']); 
    $("#terms_and_conditions").val(response['result']['terms_and_conditions']);
    $("#data-due_date").text(response['result']['due_date']); 
    $("#due_date").val(response['result']['due_date']);
    $("#data-bank_details").text(response['result']['bank_details']); 
    $("#bank_details").val(response['result']['bank_details']);
    $("#data-bcc_email").text(response['result']['bcc_email']); 
    $("#bcc_email").val(response['result']['bcc_email']);    
};
function error(){};
var params = { 'owner' : current_ctx};
jsonrpc('invoicepref.info', params, success, error);
//xxxxxxxxxxxxxxxxxxxxxxxxEnd Get Invoice Preference Infoxxxxxxxxxxxxxxxxxxxxxxx

//***********************Changed Input Field Value******************************
$('.changed-data').change(function(){ 
    changed_values[$(this).attr('id')] = $(this).val(); 
});
//xxxxxxxxxxxxxxxxxxxxxxxxEnd Changed Input Field Valuexxxxxxxxxxxxxxxxxxxxxxxxx
