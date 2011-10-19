//*****************************Global Section***********************************
var picture = null;
var resource_list = {};
var state = 0;
var states = {'enabled':1, 'host_only':2, 'repairs':4};
//xxxxxxxxxxxxxxxxxxxxxxxxxxxEnd Global Sectionxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

//****************************List Resource*************************************
function success(res) {
    $('#resource-tmpl').tmpl(res['result']).appendTo('#resource_list');
    for(resc in res['result']){
        res['result'][resc]['flag'] = res['result'][resc]['state']['enabled']?1:0;
        res['result'][resc]['flag'] |= res['result'][resc]['state']['host_only']?2:0;
        res['result'][resc]['flag'] |= res['result'][resc]['state']['repairs']?4:0;
        resource_list[res['result'][resc]['id']] = res['result'][resc];
        if(!res['result'][resc]['time_based'])
            $("#clock_"+res['result'][resc]['id']).hide();
    }
};
function error(){};
jsonrpc('resource.list', {'owner':current_ctx}, success, error);
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

//*****************************On Resource Type Click***************************
function show_resource(){
    $(this).attr('class', 'resource_type-show');
    var type = ($(this).val()).toLowerCase();
    $('.typed_resource-hidden').each(function(){
        res_id = parseInt($(this).attr('id').split('_')[1]);
        if(resource_list[res_id]['type'] == type){
            $(this).removeClass("typed_resource-hidden");
            $(this).addClass("typed_resource-visible");
        }
        if($(this).hasClass('typed_resource-visible') && $(this).hasClass('filtered_resource-visible')){
            $(this).removeClass("resource-hidden");
            $(this).addClass("resource-visible");
        }
        else{
            $(this).addClass("resource-hidden");
            $(this).removeClass("resource-visible");
        }
    });
    $('.resource_type-show').click(hide_resource);
}
function hide_resource(){
    $(this).attr('class', 'resource_type-hide');
    type = ($(this).val()).toLowerCase();
    $('.typed_resource-visible').each(function(){
        res_id = parseInt($(this).attr('id').split('_')[1]);
        if(resource_list[res_id]['type'] == type){
            $(this).addClass("typed_resource-hidden");
            $(this).removeClass("typed_resource-visible");
            $(this).addClass("resource-hidden");
            $(this).removeClass("resource-visible");
        }
    });
    $('.resource_type-hide').click(show_resource);
}
$('.resource_type-hide').click(show_resource);
$('.resource_type-show').click(hide_resource);
//xxxxxxxxxxxxxxxxxxxxxxxxxxxxEnd On Resource Type Clickxxxxxxxxxxxxxxxxxxxxxxxx

//***************************On Resource Filter Click***************************
function show_filtered_resources(){
    $(this).attr('class', 'resource_filter-show');
    $('.resource_filter-show').click(hide_filtered_resources);
    state |= states[$(this).attr('id')];
    $('.filtered_resource-visible').each(function(){
        res_id = parseInt($(this).attr('id').split('_')[1]);
        if((resource_list[res_id]['flag'] & state) != state){
            $(this).removeClass("filtered_resource-visible");
            $(this).addClass("filtered_resource-hidden");
            $(this).removeClass("resource-visible");
            $(this).addClass("resource-hidden");
        }
    });
}
function hide_filtered_resources(){
    $(this).attr('class', 'resource_filter-hide');
    $('.resource_filter-hide').click(show_filtered_resources);
    state ^= states[$(this).attr('id')];
    $('.filtered_resource-hidden').each(function(){
        res_id = parseInt($(this).attr('id').split('_')[1]);
        if((resource_list[res_id]['flag'] & state) == state){
            $(this).addClass("filtered_resource-visible");
            $(this).removeClass("filtered_resource-hidden");
        }
        if($(this).hasClass('typed_resource-visible') && $(this).hasClass('filtered_resource-visible')){
            $(this).removeClass("resource-hidden");
            $(this).addClass("resource-visible");
        }
        else{
            $(this).addClass("resource-hidden");
            $(this).removeClass("resource-visible");
        }
    });
}
$('.resource_filter-hide').click(show_filtered_resources);
$('.resource_filter-show').click(hide_filtered_resources);
//xxxxxxxxxxxxxxxxxxxxxxxxxxEnd On Resource Filter Clickxxxxxxxxxxxxxxxxxxxxxxxx
