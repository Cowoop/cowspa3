//*****************************Global Section***********************************
var picture = null;
var resource_list = {};
var state = 0;
var checked_map = {'checked':true, 'on':true, undefined:false};
var states = {'enabled':1, 'host_only':2, 'repairs':4};
var image_size_limit = 256000;//256kb
var res_id = null;
//xxxxxxxxxxxxxxxxxxxxxxxxxxxEnd Global Sectionxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

//****************************List Resource*************************************
function ImageNotAvailable(source){
    $("#"+source.id).hide();
    return true;
}
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
    setup_routing();
};
function error(){};
jsonrpc('resource.list', {'owner':current_ctx}, success, error);
//xxxxxxxxxxxxxxxxxxxxxxxxxxxEnd List Resourcexxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
//*****************************Routing******************************************
function setup_routing () {
    var routes = {
        '/:id': {
            '/edit' : resource_editing,
            on: act_on_route
        },
    };
    Router(routes).configure({ recurse: 'forward' }).init();
};
function act_on_route(id) {
    res_id = id;
};
//xxxxxxxxxxxxxxxxxxxxxxxxxxxEnd Routing****************************************
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
    $(this).unbind('click');
    $(this).attr('class', 'resource_filter-show');
    $(this).click(hide_filtered_resources);
}
function hide_filtered_resources(){
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
    $(this).unbind('click');
    $(this).attr('class', 'resource_filter-hide');
    $(this).click(show_filtered_resources);
}
$('.resource_filter-hide').click(show_filtered_resources);
$('.resource_filter-show').click(hide_filtered_resources);
//xxxxxxxxxxxxxxxxxxxxxxxxxxEnd On Resource Filter Clickxxxxxxxxxxxxxxxxxxxxxxxx

//*******************************Edit Resource**********************************
$("#resource_edit_form #update_resource-btn").click(function(){
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
            $("#picture_"+res_id).show();
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
        $("#resource_edit").hide();
        $("#resource_list").show();
        $("#resource_filters").show();
        $("#resource_types").show();
        picture = null;
        history.pushState("", document.title, window.location.pathname); //To remove hash from url
    };
    function error() {
        $("#edit_resource-msg").html("<big>Error in Updating Resource. Try again</big>");
    };
    params['name'] = $("#name").val();
    params['type'] = $("#type").val();
    params['short_description'] = $("#short_desc").val();
    params['long_description'] = $("#long_desc").val();
    params['time_based'] = checked_map[$("#time_based:checked").val()];
    params['state'] = {};
    params['state']['enabled'] = checked_map[$("#state_enabled:checked").val()];
    params['state']['host_only'] = checked_map[$("#state_host_only:checked").val()];
    params['state']['repairs'] = checked_map[$("#state_repairs:checked").val()];
    if(picture)
        params['picture'] = picture;
    jsonrpc('resource.update', params, success, error); 
});
$("#resource_edit_form #cancel-btn").click(function(){
    $("#resource_edit").hide();
    $("#resource_list").show();
    $("#resource_filters").show();
    $("#resource_types").show();
    history.pushState("", document.title, window.location.pathname); //To remove hash from url
});
function resource_editing(){
    $("#name").val(resource_list[res_id]['name']);
    $("#type option[value='" + resource_list[res_id]['type'] + "']").attr('selected', 'selected');
    $("#short_desc").val(resource_list[res_id]['short_description']);
    $("#long_desc").val(resource_list[res_id]['long_description']);
    $("#time_based").attr('checked', resource_list[res_id]['time_based']);
    $("#state_enabled").attr('checked', resource_list[res_id]['state']['enabled']);
    $("#state_host_only").attr('checked', resource_list[res_id]['state']['host_only']);
    $("#state_repairs").attr('checked', resource_list[res_id]['state']['repairs']);
    $("#resource_list").hide();
    $("#resource_filters").hide();
    $("#resource_types").hide();
    $("#resource_edit").show();
};
//xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxEnd Edit Resourcexxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
