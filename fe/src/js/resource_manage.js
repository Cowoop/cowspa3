//*****************************Global Section***********************************
var picture = null;
var resource_list = {};
var state = 0;
var checked_map = {'checked':true, undefined:false};
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
    $(".edit-link").click(resource_editing);  
};
function error(){};
jsonrpc('resource.list', {'owner':current_ctx}, success, error);
//xxxxxxxxxxxxxxxxxxxxxxxxxxxEnd List Resourcexxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

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

//*******************************Edit Resource**********************************
function resource_editing(){
    var res_id = parseInt($(this).attr('id').split('_')[1]);
    $("#name").val(resource_list[res_id]['name']);
    $("#type option[value='" + resource_list[res_id]['type'] + "']").attr('selected', 'selected');
    $("#short_desc").val(resource_list[res_id]['short_description']);
    $("#long_desc").val(resource_list[res_id]['long_description']);
    $("#time_based").attr('checked', resource_list[res_id]['time_based']);
    $("#state_enabled").attr('checked', resource_list[res_id]['state']['enabled']);
    $("#state_host_only").attr('checked', resource_list[res_id]['state']['host_only']);
    $("#state_repairs").attr('checked', resource_list[res_id]['state']['repairs']);
    $("#resource_edit").dialog({
        title: "Edit Resource", 
        width: 500, 
        buttons: {
            "Save": function() { 
                        var params = {'res_id': res_id};
                        function success(resp) {
                            resource_list[res_id]['name'] = params['name'];
                            $("#edit_"+params['res_id']).text(params['name']);
                            resource_list[res_id]['type'] = params['type'];
                            resource_list[res_id]['short_description'] = params['short_description'];
                            $("#short_description_"+params['res_id']).text(params['short_description']);
                            resource_list[res_id]['state'] = params['state']
                            resource_list[res_id]['long_description'] = params['long_description'];
                            resource_list[res_id]['flag'] = resource_list[res_id]['state']['enabled']?1:0;
                            resource_list[res_id]['flag'] |= resource_list[res_id]['state']['host_only']?2:0;
                            resource_list[res_id]['flag'] |= resource_list[res_id]['state']['repairs']?4:0;
                            resource_list[res_id]['time_based'] = params['time_based'];
                            if(picture){
                                resource_list[res_id]['picture'] = picture;
                                $("#picture_"+res_id).attr('src', picture);
                            }
                            
                            if(resource_list[res_id]['time_based'])
                                $("#clock_"+res_id).show();
                            else
                                $("#clock_"+res_id).hide();
                            if((resource_list[res_id]['flag'] & state) != state){
                                $("#resource_"+res_id).removeClass("filtered_resource-visible");
                                $("#resource_"+res_id).addClass("filtered_resource-hidden");
                            }
                            if(!$("#rtype_"+resource_list[res_id]['type']).hasClass('resource_type-show')){
                                $("#resource_"+res_id).removeClass("typed_resource-visible");
                                $("#resource_"+res_id).addClass("typed_resource-hidden");
                            }
                            if(!$("#resource_"+res_id).hasClass('typed_resource-visible') || !$("#resource_"+res_id).hasClass('filtered_resource-visible')){
                                $("#resource_"+res_id).addClass("resource-hidden");
                                $("#resource_"+res_id).removeClass("resource-visible");
                            }
                            
                            $("#resource_edit").dialog("close"); 
                            $("#edit_resource-msg").html("");
                            picture = null;
                        };
                        function error() {
                            $("#edit_resource-msg").html("<big>Error in Updating Resource. Try again</big>");
                        };
                        params['name'] = $("#name").val();
                        params['type'] = $("#type").val();
                        params['short_description'] = $("#short_desc").val();
                        params['long_description'] = $("#long_desc").val();
                        params['time_based'] = checked_map[$("#time_based").attr('checked')];
                        params['state'] = {};
                        params['state']['enabled'] = checked_map[$("#state_enabled").attr('checked')];
                        params['state']['host_only'] = checked_map[$("#state_host_only").attr('checked')];
                        params['state']['repairs'] = checked_map[$("#state_repairs").attr('checked')];
                        if(picture)
                            params['picture'] = picture;
                        jsonrpc('resource.update', params, success, error);  
                    }, 
            "Cancel": function() { 
                        $(this).dialog("close"); 
                        $("#edit_resource-msg").html("");
                        picture = null;
                      }
            } 
    });  
};
//xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxEnd Edit Resourcexxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
