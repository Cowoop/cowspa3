var thismember = null;
var thismember_id = null;
var is_get_thismember_usages_done = false;
var is_get_thismember_invoices_done = false;
var is_get_thismember_billingpref_done = false;
var select_member_box = $('.select-member');
var usage_table;
var invoice_table;
var usage_edit_id = null;
var mtype = null;
var invoice_send_link_id;
var invoice_email_text;

function on_member_profile(resp) {
    thismember = resp.result;
    mtype = thismember.mtype;
    $(".action-status").removeClass('status-success');
    $(".action-status").removeClass('status-failed');
    $(".action-status").text("");
    
    if(mtype == "individual"){
        $(".individual").show();
        $(".organization").hide();
        $('input[name="first_name"]').attr("required","");
        $('input[name="name"]').removeAttr("required");
    }
    else{
        $('input[name="first_name"]').removeAttr("required");
        $('input[name="name"]').attr("required","");
        $(".individual").hide();
        $(".organization").show();
    }
    $('.content-title').show();
    $('#content-title').text(thismember.profile.name);
    $('.data-id').text(thismember_id);
    $('.data-username').text(thismember.account.username);
    $('.data-work').text(thismember.contact.work);
    $('.data-home').text(thismember.contact.home);
    $('.data-mobile').text(thismember.contact.mobile);
    $('input[name="first_name"]').val(thismember.profile.first_name);
    $('input[name="name"]').val(thismember.profile.name);
    $('input[name="company_no"]').val(thismember.profile.company_no);
    $('input[name="last_name"]').val(thismember.profile.last_name);
    $('input[name="short_description"]').val(thismember.profile.short_description);
    $('textarea[name="long_description"]').val(thismember.profile.long_description);
    $('textarea[name="address"]').val(thismember.contact.address);
    $('input[name="city"]').val(thismember.contact.city);
    $('input[name="province"]').val(thismember.contact.province);
    $('input[name="email"]').val(thismember.contact.email);
    $('input[name="work"]').val(thismember.contact.work);
    $('input[name="home"]').val(thismember.contact.home);
    $('input[name="mobile"]').val(thismember.contact.mobile);
    $('input[name="fax"]').val(thismember.contact.fax);
    $('.data-email-link').attr('href', 'mailto:'+thismember.contact.email).text(thismember.contact.email);
    $('#country').val(thismember.contact.country);
    $('#member-info').slideDown();
    $('input[name="username"]').val(thismember.account.username);
    $('select[name="theme"]').val(thismember.preferences.theme);
    $('select[name="language"]').val(thismember.preferences.language);
    $('.data-membership').text(thismember.memberships.length>0?thismember.memberships[0].tariff_name:"-");
    for(i in thismember.memberships){
        thismember.memberships[i].starts = isodate2fdate(thismember.memberships[i].starts);
        thismember.memberships[i].ends = isodate2fdate(thismember.memberships[i].ends);
    }
    $('#tariff-row').tmpl(thismember.memberships).appendTo('#tariff-info');
    bind_cancel_and_change_tariff();
    var base_url = "/" + thismember.preferences.language + "/" + thismember.preferences.theme + '/member/edit/#/';
    $('#st-about').attr('href', base_url + thismember_id + '/about');
    $('#st-contact').attr('href', base_url + thismember_id + '/contact');
    $('#st-billing').attr('href', base_url + thismember_id + '/billing');
    $('#st-memberships').attr('href', base_url + thismember_id + '/memberships');
};

function act_on_route(id) {
    if (thismember_id != parseInt(id, 10)) {
        thismember_id = parseInt(id, 10);
        is_get_thismember_usages_done = false;
        is_get_thismember_invoices_done = false;
        is_get_thismember_billingpref_done = false;
        select_member_box.hide();
        var params = {'member_id': id, 'bizplace_ids': [parseInt(current_ctx, 10)]};
        jsonrpc('member.profile', params, on_member_profile);
    };
};

//********************************Tabs******************************************
$("#profile_tabs").tabs({
    collapsible:false,
});
$(".profile-tab").click(function(){ 
    window.location.hash = "#/" + thismember_id + "/" + $(this).attr('href').slice(1);
});
//-------------------------------End Tabs---------------------------------------
function show_info() { $("#profile_tabs").tabs('select', 0); };
function show_profile() { $("#profile_tabs").tabs('select', 1); };
function show_memberships() {
    $('.tariff_row').remove();
    $('#tariff-loading').show();
    $("#profile_tabs").tabs('select', 2); 
    load_tariff_records();
};
function show_billing() {
    $("#billing .action-status").text("").removeClass('status-fail status-success');
    if(!is_get_thismember_billingpref_done && mtype!="Organization"){
        get_billing_preferences();
        get_billing_pref_details();
    };
    if(mtype != "Organization"){
        $("#profile_tabs").tabs('select', 3);
    } 
};
function show_usages() {
    if(!is_get_thismember_usages_done){
        get_uninvoiced_usages();
    };
    $("#profile_tabs").tabs('select', 4);
    $("#add_usage").hide();
    $("#edit_usage").hide(); 
    $("#uninvoiced_usages").show();
};
function show_add_usage() {
    $("#profile_tabs").tabs('select', 4);
    $("#uninvoiced_usages").hide();
    $("#edit_usage").hide();
    if($("#resource_select option:selected").text()=="Custom"){
        $("#calculate_cost-btn").attr("disabled",true);
        $("#submit-usage").removeAttr("disabled");
    }
    else{
        $("#submit-usage").attr("disabled", true);
        $("#calculate_cost-btn").removeAttr("disabled");
    };
    $("#add_usage").show();
};
function show_edit_usage(id, usage_id) {
    $("#profile_tabs").tabs('select', 4);
    $("#uninvoiced_usages").hide();
    $("#add_usage").hide();
    $("#edit_usage").show();
    handle_edit_usage(usage_id);
};
function show_invoices() {
    $("#profile_tabs").tabs('select', 5);
    if(!is_get_thismember_invoices_done){
        get_invoice_tab_data();
    };
};

function setup_routing () {
    var routes = {
        '/:id': {
            '/info': show_info,
            '/profile': show_profile,
            '/billing': show_billing,
            '/memberships': show_memberships,
            '/usages/new' : show_add_usage,
            '/usages/:usage_id/edit' : show_edit_usage,
            '/usages': show_usages,
            '/invoices': show_invoices,
            on: act_on_route
        },
    };
    Router(routes).configure({ recurse: 'forward' }).init();
};
setup_routing();

function edit_member(theform) {
    var action_status = $('#'+theform.attr('id') + ' .action-status');
    if(mtype == "individual"){
        $('input[name="name"]').val($('input[name="first_name"]').val()+" "+$('input[name="last_name"]').val());
    }
    var inputs = theform.serializeArray();
    var params = {'member_id': thismember_id}
    for(var i in inputs) {
        if(inputs[i].name=="password" && jQuery.trim(inputs[i].value)=="")
            continue;
        params[inputs[i].name] = inputs[i].value;
    };
    function success(resp) {
        $('.action-status').text("").removeClass('status-fail');
        $('.action-status').removeClass('status-success');
        action_status.text("Update is successful.").addClass('status-success');
        $('.data-username').text($("#username").val());
        $('.data-email-link').attr('href', 'mailto:'+$("#member-contact-edit-email").val()).text($("#member-contact-edit-email").val());
        $('#content-title').text($('input[name="name"]').val());
        if("theme" in params && params.theme!=thismember.preferences.theme){
            window.location = (window.location).toString().replace(thismember.preferences.theme.toString(), params.theme.toString());
        }
    };
    function error() {
        $('.action-status').text("").removeClass('status-fail');
        $('.action-status').removeClass('status-success');
        action_status.text("Update failed").addClass('status-fail');
    };
    action_status.text("updating ...");
    jsonrpc('member.update', params, success, error);
};

$('.profile-edit-form').submit(function () {
    var theform = $(this);
    theform.checkValidity();
    edit_member(theform);
    return false;
});

//*************************Billing Preferences**********************************
var mode, billto, details;
$("#billing_pref .mode").click(function(){
    $("#details_1").hide();
    $("#details_2").hide();
    $("#billing_details").show();
    mode = $(this).val();
    $("#details_"+mode).show();
    if(mode == "0"){
        $("#billing_details").hide();
    }
    $("#billing .action-status").text("").removeClass('status-fail');
    $("#billing .action-status").removeClass('status-success');
});
//---------------------Save Billing Preferences---------------------------------
$("#update-billingpref").click(function(){
    var params = {'member': thismember_id, 'mode': parseInt(mode, 10)};
    switch(parseInt(mode, 10)){
        case 0 : params['billto'] = null;
                 break;
        case 1 : params['billto'] = null;
                 params['details'] = {
                    "name" :$("#details_1 #custom_name").val(),
                    "address" :$("#details_1 #custom_address").val(),
                    "city" :$("#details_1 #custom_city").val(),
                    "country" :$("#details_1 #custom_country").val(),
                    "phone" :$("#details_1 #custom_phone").val(),
                    "email" :$("#details_1 #custom_email").val()
                    };
                 break;
        case 2 : params['billto'] = billto;
                 break;         
    }
    function on_save_billingpref_success(){
        $("#billing .action-status").removeClass('status-fail');
        $("#billing .action-status").text("Billing Preferences Saved Successfully.").addClass('status-success');
        get_billing_pref_details();
    };
    function on_save_billingpref_error(){
        $("#billing .action-status").removeClass('status-success');
        $("#billing .action-status").text("Save billing preferences fail.").addClass('status-fail');
    };
   
    jsonrpc('billingpref.update', params, on_save_billingpref_success, on_save_billingpref_error);
});
//------------------Get Billing Preferences-------------------------------------
function get_billing_preferences(){
    function on_get_billingpref_success(resp){
        mode = resp['result']['mode']; 
        billto = resp['result']['billto'];
        details = resp['result']['details'];
        switch(mode){
            case 0 : $('input:radio[name=mode][value=0]').click();
                     break;
            case 1 : $('input:radio[name=mode][value=1]').click();
                     if(details != null){
                        $('#details_1 #custom_name').val(details['name']);
                        $('#details_1 #custom_address').val(details['address']);
                        $('#details_1 #custom_city').val(details['city']);
                        $("#details_1 #custom_country option[value='" + details['country'] + "']").attr('selected', 'selected');
                        $('#details_1 #custom_phone').val(details['phone']);
                        $('#details_1 #custom_email').val(details['email']);
                     }
                     break;
            case 2 : $('input:radio[name=mode][value=2]').click();
                     break;
        }   
        is_get_thismember_billingpref_done = true;
    };
    function on_get_billingpref_error(){};
    var params = {'member': thismember_id};
    jsonrpc('billingpref.info', params, on_get_billingpref_success, on_get_billingpref_error);
};
//-------------------------Get Billing Preferences Details----------------------
function get_billing_pref_details(){
    function on_success(resp){
        if(mode==2){
            $('#details_2 #member').val(resp['result']['name']);
        };
    };
    function on_error(){};
    var args = {'member': thismember_id};
    jsonrpc('billingpref.details', args, on_success, on_error);
};
//------------------------Existing Member Search--------------------------------
$('#details_2 #member').autocomplete({
    source: "/search/member", 
    select: function (event, ui) {
        billto = ui.item.id;
    } 
});
//************************End of Billing Preferences****************************
// ***************************Next Tariff***************************************
 
$('#next-tariff-form #start-vis').datepicker( {
    altFormat: 'yy-mm-dd',
    altField: '#start',
    dateFormat: 'M d, yy',
    showButtonPanel: true,
});
$('#next-tariff-form #end-vis').datepicker( {
    altFormat: 'yy-mm-dd',
    altField: '#end',
    dateFormat: 'M d, yy',
    showButtonPanel: true,
    beforeShow: function( input ) {
        setTimeout(function() {
            var buttonPane = $( input ).datepicker( "widget" ).find( ".ui-datepicker-buttonpane" );
            $( "<button>", {
                text: "Clear",
                class: 'ui-datepicker-close ui-state-default ui-priority-primary ui-corner-all',
                click: function() {
                    $.datepicker._clearDate( input );
                }
            }).appendTo( buttonPane );
        }, 1);
    }
});
$('#next_tariff-btn').click(function() {
    $("#next-tariff-form .action-status").text("").removeClass('status-fail');
    $('#next-tariff-form #start-vis').datepicker("setDate", null);
    $('#next-tariff-form #end-vis').datepicker("setDate", null);
    $('#next-tariff-form').dialog({ 
        title: "Next Tariff", 
        width: 500, 
    });
});
function save_next_tariff() { 
    var params = {}
    function success(resp) {
        $("#next-tariff-form").dialog("close"); 
        window.location.reload();
        $("#next-tariff-form .action-status").text("").removeClass('status-fail');
        is_get_thismember_usages_done = false;
    };
    function error(resp) {
        $("#next-tariff-form .action-status").text(resp.error.data).addClass("status-fail");
    };
    params['member_id'] = thismember_id;
    params['tariff_id'] = $("#next-tariff-form #tariff").val();
    params['starts'] = $("#next-tariff-form #start").val();
    params['ends'] = $("#next-tariff-form #end").val();
    $("#next-tariff-form .action-status").text("").removeClass('status-fail');
    jsonrpc('memberships.new', params, success, error);
};
$("#next-tariff-form").submit(function () {
    $(this).checkValidity();
    save_next_tariff();
    return false;
});
$("#tariff_cancel-btn").click(function() { 
    $("#next-tariff-form").dialog("close"); 
}); 

function success1(resp) {
    var tariffs = resp.result;
    for(ind in tariffs)
        if(tariffs[ind].name == "Guest Tariff"){
            delete(tariffs[ind]);
            break;
        };
    $("#tariff-options").tmpl(resp['result']).appendTo( "#next-tariff-form #tariff" );
    $("#tariff-options").tmpl(resp['result']).appendTo( "#change-tariff-form #tariff" );
    };
jsonrpc('tariffs.list', {owner: current_ctx}, success1);
    
//*************************End Next Tariff**************************************


//**************************Tariff History**************************************
function load_tariff_records() {
    var params = {}
    function success(response) {
        memberships = response.result;
        for(i in memberships){
            memberships[i].starts = isodate2fdate(memberships[i].starts);
            memberships[i].ends = isodate2fdate(memberships[i].ends);
        }
        $('#tariff-row').tmpl(response.result).appendTo('#tariff-list');
        $('#tariff-list').show();
        $('#load-tariff-history').hide();
        bind_cancel_and_change_tariff();
        $('#tariff-loading').hide();
    };
    function error(resp){
        alert("Error loading memberships: " + resp.error.message);
    };
    params['for_member'] = thismember_id;
    params['bizplace_ids'] = [parseInt(current_ctx, 10)];
    jsonrpc('memberships.list', params, success, error); 
};
//***************************End Tariff History*********************************
//************************Cancel/Change Tariff**********************************
$('#change-tariff-form #starts-vis').datepicker( {
    altFormat: 'yy-mm-dd',
    altField: '#change-tariff-form #starts',
    dateFormat: 'M d, yy',
    showButtonPanel: true
});
//Clear button code:http://jsbin.com/ofare/edit#javascript,html,live
$('#change-tariff-form #ends-vis').datepicker( {
    altFormat: 'yy-mm-dd',
    altField: '#change-tariff-form #ends',
    dateFormat: 'M d, yy',
    showButtonPanel: true,
    beforeShow: function( input ) {
        setTimeout(function() {
            var buttonPane = $( input ).datepicker( "widget" ).find( ".ui-datepicker-buttonpane" );
            $( "<button>", {
                text: "Clear",
                class: 'ui-datepicker-close ui-state-default ui-priority-primary ui-corner-all',
                click: function() {
                    $.datepicker._clearDate( input );
                }
            }).appendTo( buttonPane );
        }, 1);
    }
});

function bind_cancel_and_change_tariff() {
    $('.cancel-sub').unbind('click');
    $('.cancel-sub').click(function(){
        var params = {'membership_id': $(this).attr('id').split("-")[1]};
        function success(response) {
            $("#tariff_row-"+params['membership_id']).hide();
            is_get_thismember_usages_done = false; 
        };
        function error(){};
        if(confirm("Do you want to remove?")){
            jsonrpc('membership.delete', params, success, error);
        }
    });
    $('.change-sub').unbind('click');
    $('.change-sub').click(function(){
        var membership_id = $(this).attr('id').split("-")[1];
        var date = fdate2date($("#tariff_row-"+membership_id+" #starts").text());
        $('#change-tariff-form #starts-vis').datepicker("setDate", date);
        if($("#tariff_row-"+membership_id+" #ends").text()!=""){
            date = fdate2date($("#tariff_row-"+membership_id+" #ends").text());
            $('#change-tariff-form #ends-vis').datepicker("setDate", date);
        }
        else{
            $('#change-tariff-form #ends-vis').datepicker("setDate", null);
        }
        //$("#change-tariff-form #tariff option:contains('" + $("#tariff_row-"+membership_id+" #tariff_name").text() + "')").attr('selected', 'selected');
        $('#change-tariff-form').dialog({ 
            title: "Change Tariff", 
            width: 500, 
        });
        $("#change-tariff-form #save-btn").unbind('click');
        $("#change-tariff-form #save-btn").click(function() { 
            var params = {'membership_id':membership_id};
            //params['tariff_id'] = $("#change-tariff-form #tariff").val();
            //params['tariff_name'] = $("#change-tariff-form #tariff option[value='"+params['tariff_id']+"']").text();
            params['starts'] = $('#change-tariff-form #starts').val();
            if($('#change-tariff-form #end').val() != ""){
                params['ends'] = $('#change-tariff-form #ends').val();
            }
            function success(resp) { 
                $("#tariff_row-"+membership_id+" #starts").text(isodate2fdate(params.starts));
                $("#tariff_row-"+membership_id+" #ends").text(isodate2fdate(params.ends));
                $("#change-tariff-form .action-status").text("").removeClass("status-success status-fail");
                $('#change-tariff-form').dialog("close");
                is_get_thismember_usages_done = false;
            };
            function error() {
                $("#change-tariff-form .action-status").text("Error in Changing Tariff. Try again").addClass("status-fail");
            };
            jsonrpc('membership.update', params, success, error);
        }); 
        $("#change-tariff-form #cancel-btn").unbind('click');
        $("#change-tariff-form #cancel-btn").click(function() { 
            $('#change-tariff-form').dialog("close");
            $("#change-tariff-form .action-status").text("").removeClass("status-fail status-success");
        }); 
    });
};   
//***********************End Cancel/Change Tariff*******************************
//****************************Usage Management********************************** 
//-----------------------------Get Resources------------------------------------
function on_get_resources_success(res) {
    $('#resource-tmpl').tmpl(res['result']).appendTo('#add-usage-form #resource_select');
    $('#resource-tmpl').tmpl(res['result']).appendTo('#edit_usage-form #res_select');
    var custom_resource = [{'id':0, 'name':'Custom'}];
    $('#resource-tmpl').tmpl(custom_resource).appendTo('#add-usage-form #resource_select');
    $('#resource-tmpl').tmpl(custom_resource).appendTo('#edit_usage-form #res_select');
    $("#resource_name").val($("#add-usage-form #resource_select option:first").text());
};
function on_get_resources_error(){};
jsonrpc('resources_and_tariffs.list', {'owner':current_ctx}, on_get_resources_success, on_get_resources_error);
//--------------------------------Add Usage-------------------------------------
$("#add_usage [for='cost']").text($("[for='cost']").text()+' (' +locale_data.currency_symbol+')');
$("#resource_select").change(function(){
    $("#resource_name").val($("#resource_select option:selected").text());
    if($("#resource_select option:selected").text()=="Custom"){
        $("#calculate_cost-btn").attr("disabled",true);
        $("#submit-usage").removeAttr("disabled");
    }
    else{
        $("#submit-usage").attr("disabled", true);
        $("#calculate_cost-btn").removeAttr("disabled");
    };
});
$('#add-usage-form #start_time').datetimepicker({
    ampm: true,
    dateFormat: 'M d, yy',
    timeFormat: 'hh:mm TT',
});
$('#add-usage-form #end_time').datetimepicker({
    ampm: true,
    dateFormat: 'M d, yy',
    timeFormat: 'hh:mm TT',
});
$("#calculate_cost-btn").click(function(){
    params = {
        'resource_id' : parseInt($("#resource_select").val(), 10),
        'resource_owner' : parseInt(current_ctx, 10),
        'quantity' : parseFloat($("#quantity").val()),
        'member_id' : thismember_id,
        'starts' : fdate2iso($("#start_time").val()),
        'ends' : fdate2iso($("#end_time").val())
    };
    function on_calculate_cost_success(resp){
        $("#cost").val(resp.result.calculated_cost);
        $("#submit-usage").removeAttr("disabled"); 
        $("#add-usage-form .action-status").text("").removeClass('status-fail status-success');
    };
    function on_calculate_cost_error(){
        $("#add-usage-form .action-status").text("Cost Calculation fail.").addClass('status-fail');
    };
    if($('#add-usage-form').checkValidity()){
        jsonrpc('pricing.calculate_cost', params, on_calculate_cost_success, on_calculate_cost_error);
    }
    else{
        $("#add-usage-form .action-status").text("Fill the all required fields.").addClass('status-fail');
    }
});
$('#submit-usage').click(function(){
    var action_status = $('#add-usage-form .action-status');
    params = {
        'resource_id' : parseInt($("#resource_select").val(), 10),
        'resource_name' : $("#resource_name").val(),
        'resource_owner' : parseInt(current_ctx, 10),
        'quantity' : parseFloat($("#quantity").val()),
        'cost' : parseFloat($("#cost").val()),
        'member' : thismember_id,
        'start_time' : fdate2iso($("#start_time").val()),
        'end_time' : fdate2iso($("#end_time").val())
    };
    function on_add_usage_success(resp){
        action_status.text("Add usage is successful.").addClass('status-success');
        $("#resource_select").show();
        $("#resource_name").hide();
        $("#submit-usage").attr("disabled", true);
        get_uninvoiced_usages();
        window.location.hash = "/" + thismember_id + "/usages";
        action_status.text("").removeClass('status-fail status-success');
    };
    function on_add_usage_error(){
        action_status.text("Add usage fail.").addClass('status-fail');
    };
    if($('#add-usage-form').checkValidity()){
        jsonrpc('usage.new', params, on_add_usage_success, on_add_usage_error);
    }
    else{
        $("#add-usage-form .action-status").text("Fill the all required fields.").addClass('status-fail');
    }
});
$("#new_usage-btn").click(function(){
    window.location.hash = "/" + thismember_id + "/usages/new";
});
$(".cancel-usage").click(function(){
    window.location.hash = "/" + thismember_id + "/usages";
    $('#add-usage-form .action-status').text("").removeClass('status-fail status-success');
    $('#edit_usage-form .action-status').text("").removeClass('status-fail status-success');
});
//-----------------------------Uninvoiced Usages--------------------------------
function get_uninvoiced_usages(){
    function success(response){
        is_get_thismember_usages_done = true;
        var aaData = [];
        for (var i=0; i < response.result.length; i++) {
            var item = response.result[i];
            aaData[i] = [item.resource_name, item.start_time, item.end_time, item.quantity, item.cost, item.id];
        };
        usage_table = $('#usage_table').dataTable({
            "aaData": aaData,
            "bJQueryUI": true,
            "bAutoWidth": false,
            "bDestroy": true,
            "sPaginationType": "full_numbers",
            "aoColumns": [
                { "sTitle": "Resource/Tariff Name", "sWidth":"20%" },
                { "sTitle": "Start Time", "sWidth":"20%",
                    "fnRender": function(obj) {
                        var sReturn = obj.aData[obj.iDataColumn];
                        return iso2fdate(sReturn);
                        }
                },
                { "sTitle": "End Time", "sWidth":"20%",
                    "fnRender": function(obj) {
                        var sReturn = obj.aData[obj.iDataColumn];
                        return iso2fdate(sReturn);
                        }
                },
                { "sTitle": "Quantity", "sWidth":"10%"},
                { "sTitle": "Cost",  "sWidth":"10%",
                    "fnRender": function(obj) {
                            var sReturn = format_currency(obj.aData[ obj.iDataColumn ]);
                            return sReturn;
                    }
                },
                { "sTitle": "Manage", "bSortable": false, "sWidth":"10%",
                    "fnRender": function(obj) {
                        var usage_id = obj.aData[obj.iDataColumn];
                        var data = {'thismember_id':thismember_id, 'usage_id':usage_id};
                        var edit_link = "<A id='edit_usage-"+usage_id+"' href='#/"+thismember_id+"/usages/"+usage_id+"/edit'>Edit</A>";
                        var cancel_link = "<A id='cancel_usage-"+usage_id+"' href='#/"+thismember_id+"/usages' class='delete-usage'>X</A>";
                        return edit_link + "<c> | </c>" + cancel_link;
                        }
                },
            ]
        });
        $(".delete-usage").click(delete_usage);
    };
    function error(){};
    var params = { 'member_ids' : [thismember_id], 'uninvoiced':true, 'res_owner_ids':[parseInt(current_ctx, 10)]};
    jsonrpc('usages.find', params, success, error);
};
//---------------------------Edit Usage-----------------------------------------
$("#res_select").change(function(){
    $("#res_name").val($("#res_select option:selected").text());
    if($("#res_select option:selected").text()=="Custom"){
        $("#recalculate_cost-btn").attr("disabled",true);
    }
    else{
        $("#recalculate_cost-btn").removeAttr("disabled");
    };
});
$('#edit_usage-form #res_start_time').datetimepicker({
    ampm: true,
    dateFormat: 'M d, yy',
    timeFormat: 'hh:mm TT',
});
$('#edit_usage-form #res_end_time').datetimepicker({
    ampm: true,
    dateFormat: 'M d, yy',
    timeFormat: 'hh:mm TT',
});
$("#edit_usage [for='res_cost']").text($("[for='res_cost']").text()+' (' +locale_data.currency_symbol+')');
function handle_edit_usage(usage_id){
    usage_edit_id = usage_id;
    function on_get_usage_info_success(response){
        info = response.result;
        if($("#edit_usage-form #res_select option:selected").text()=="Custom"){
            $("#recalculate_cost-btn").attr("disabled",true);
        }
        else{
            $("#recalculate_cost-btn").removeAttr("disabled");
        };
        $('#edit_usage-form #res_select').val(info.resource_id);
        $("#edit_usage-form #res_name").val(info.resource_name);
        $("#edit_usage-form #res_quantity").val(info.quantity);
        $("#edit_usage-form #res_start_time").val(iso2fdate(info.start_time));
        $("#edit_usage-form #res_end_time").val(iso2fdate(info.end_time));
        $("#edit_usage-form #res_cost").val(info.cost);
    };
    function on_get_usage_info_error(){
    };
    jsonrpc('usage.info', {'usage_id': parseInt(usage_id)}, on_get_usage_info_success, on_get_usage_info_error);
};
$("#recalculate_cost-btn").click(function(){
    params = {
        'resource_id' : parseInt($("#res_select").val(), 10),
        'resource_owner' : parseInt(current_ctx, 10),
        'quantity' : parseFloat($("#res_quantity").val()),
        'member_id' : thismember_id,
        'starts' : fdate2iso($("#res_start_time").val()),
        'ends' : fdate2iso($("#res_end_time").val())
    };
    function on_calculate_cost_success(resp){
       $("#res_cost").val(resp.result.calculated_cost);
       $('#edit_usage-form .action-status').text("").removeClass('status-fail status-success');
    };
    function on_calculate_cost_error(){
        $("#edit_usage-form .action-status").text("Cost calculation failed").addClass('status-fail');
    };
    if($('#edit_usage-form').checkValidity()){
        jsonrpc('pricing.calculate_cost', params, on_calculate_cost_success, on_calculate_cost_error);
    }
    else{
        $("#edit_usage-form .action-status").text("Fill the all required fields.").addClass('status-fail');
    }
});
$('#update-usage').click(function(){
    var action_status = $('#edit_usage-form .action-status');
    var params = {
        'usage_id' : parseInt(usage_edit_id, 10),
        'resource_id' : parseInt($("#res_select").val(), 10),
        'resource_name' : $("#res_name").val(),
        'quantity' : parseFloat($("#res_quantity").val()),
        'cost' : parseFloat($("#res_cost").val()),
        'start_time' : fdate2iso($("#res_start_time").val()),
        'end_time' : fdate2iso($("#res_end_time").val())
    };
    function on_edit_usage_success(resp){
        action_status.text("Update usage is successful").addClass('status-success');
        $("#resource_select").show();
        $("#resource_name").hide();
        get_uninvoiced_usages();
        window.location.hash = "/" + thismember_id + "/usages";
        $('#edit_usage-form .action-status').text("").removeClass('status-fail status-success');
    };
    function on_edit_usage_error(){
        action_status.text("Update usage fail.").addClass('status-fail');
    };
    if($('#edit_usage-form').checkValidity()){
        jsonrpc('usage.update', params, on_edit_usage_success, on_edit_usage_error);
    }
    else{
        $("#edit_usage-form .action-status").text("Fill the all required fields.").addClass('status-fail');
    }
});
//---------------------------Cancel Usage---------------------------------------
function delete_usage() {
    var row = $(this).closest("tr").get(0);
    function on_usage_cancel_success(response){
        usage_table.fnDeleteRow(usage_table.fnGetPosition(row));
    };
    function on_usage_cancel_error(){
    };
    if(confirm("Do you want to cancel usage?")){
        var params = {};
        params['usage_id'] = parseInt($(this).attr("id").split("-")[1], 10);
        jsonrpc('usages.delete', params, on_usage_cancel_success, on_usage_cancel_error);
    };
};

//xxxxxxxxxxxxxxxxxxxxxxxxxxxEnd Usage Managementxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
//********************************Invoices**************************************
function get_invoice_tab_data(){
    function get_invoice_history_success(response) {
        is_get_thismember_invoices_done = true;
        invoice_table = $('#history_table').dataTable({
            "aaData": response.result,
            "bJQueryUI": true,
            "bDestroy": true,
            "sPaginationType": "full_numbers",
            "aaSorting": [[ 0, "desc" ]],
            "aoColumns": [
                { "sTitle": "Number" },
                { "sTitle": "Amount",
                    "fnRender": function(obj) {
                            var sReturn = format_currency(obj.aData[ obj.iDataColumn ]);
                            return sReturn;
                    }
                },
                { "sTitle": "Date",
                "fnRender": function(obj) {
                        var sReturn = obj.aData[obj.iDataColumn];
                        return isodate2fdate(sReturn);
                        }   
                },
                { "sTitle": "Send",
                "fnRender": function(obj) {
                        var sent = obj.aData[obj.iDataColumn];
                        var inv_id = obj.aData[obj.iDataColumn+1];
                        var link;
                        if(sent){
                            link = "<A id='inv-"+inv_id+"' href='#/"+thismember_id+"/invoices' class='inv-send'>Resend</A>";
                        }
                        else{
                            link = "<A id='inv-"+inv_id+"' href='#/"+thismember_id+"/invoices' class='inv-send'>Send</A>";
                        }
                        return link;
                        }      
                },
                { "sTitle": "Actions", "bSortable": false,
                "fnRender": function(obj) {
                        var sent = obj.aData[obj.iDataColumn-1];
                        var inv_id = obj.aData[obj.iDataColumn];
                        if(sent){
                            link = "<A id='"+inv_id+"' href='#/"+thismember_id+"/invoices' class='invoice-view'>View</A>";
                        }
                        else{
                            link = "<A id='"+inv_id+"' href='#/"+thismember_id+"/invoices' class='invoice-view'>View</A>|<A id='delete-"+inv_id+"' href='#/"+thismember_id+"/invoices' class='invoice-delete'>X</A>";
                        }
                        return link;
                        }
                },
            ]
        });
        //****************************View Invoice**********************************
        $('.invoice-view').click(function () {
            $('#view_invoice_window #invoice-iframe').attr('src', '/invoice/'+$(this).attr('id')+'/html');
            $('#view_invoice_window').dialog({ 
                title: "Invoice", 
                width: 800,
                height: 600
            });
        });
        //xxxxxxxxxxxxxxxxxxxxxxxxxxEnd View Invoicexxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        //****************************Delete Invoice**********************************
    $('.invoice-delete').click(function () {
        var row = $(this).closest("tr").get(0);
        function on_invoice_delete_success(){
            invoice_table.fnDeleteRow(invoice_table.fnGetPosition(row));
        };
        function on_invoice_delete_error(resp){
            alert("Error in deleting invoice: "+resp.error.data);
        };
        if(confirm("Do you want to delete invoice?")){
            jsonrpc("invoice.delete", {'invoice_id':$(this).attr('id').split("-")[1]}, on_invoice_delete_success, on_invoice_delete_error);
        };
    });
        //****************************Send Invoice**********************************
    $('.inv-send').click(function () {
        $("#email_text").text(invoice_email_text);
        invoice_send_link_id = $(this).attr("id");
        $('#send_invoice-form .action-status').removeClass('status-fail');
        $('#send_invoice-form .action-status').removeClass('status-success').text("");
        $('#send_invoice-form').dialog({ 
            title: "Send Invoice",
            width: 500
        });
    });
    function on_send_invoice_success() {
        var params = { 'issuer' : parseInt(current_ctx, 10), 'member' : parseInt(thismember_id, 10), 'hashrows':false};
        jsonrpc('invoice.by_member', params, get_invoice_history_success);
        $('#send_invoice-form .action-status').removeClass('status-fail');
        $('#send_invoice-form .action-status').addClass('status-success').text('Invoice sent successfully');
    };
    function on_send_invoice_failure() {
        $('#send_invoice-form .action-status').removeClass('status-success');
        $('#send_invoice-form .action-status').addClass('status-fail').text('failed to send invoice');
    };
    $("#send-btn").click(function(){
        var params = {invoice_id : invoice_send_link_id.split("-")[1], mailtext:$("#email_text").text()};
        $('#send_invoice-form .action-status').removeClass('status-success');
        $('#send_invoice-form .action-status').removeClass('status-fail').text('sending ...');
        jsonrpc('invoice.send', params, on_send_invoice_success, on_send_invoice_failure);
    });
    $("#send_cancel-btn").click(function(){
        $('#send_invoice-form').dialog("close");
    });
    //xxxxxxxxxxxxxxxxxxxxxxxxxxEnd Delete Invoicexxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    };
    var params = { 'issuer' : parseInt(current_ctx, 10), 'member' : parseInt(thismember_id, 10), 'hashrows':false};
    jsonrpc('invoice.by_member', params, get_invoice_history_success);
    //******************************Email text************************************
    function on_get_invoicemail_cust(response) {
        invoice_email_text = response.result;
    };

    jsonrpc('messagecust.get', {owner_id: current_ctx, name: 'invoice'}, on_get_invoicemail_cust);
};
$("#new_invoice-btn").click(function(){
    window.location = basepath + '/invoices/new/#/invoicee/' + thismember_id;
});
//xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxEnd Invoicesxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

