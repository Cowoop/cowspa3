var thismember = null;
var thismember_id = null;
var select_member_box = $('.select-member');

function on_member_profile(resp) {
    thismember = resp.result;
    $('.content-title').show();
    $('#content-title').text(thismember.profile.name);
    $('.data-id').text(thismember_id);
    $('.data-username').text(thismember.account.username);
    $('input[name="first_name"]').val(thismember.profile.first_name);
    $('input[name="last_name"]').val(thismember.profile.last_name);
    $('input[name="short_description"]').val(thismember.profile.short_description);
    $('textarea[name="long_description"]').val(thismember.profile.long_description);
    $('input[name="address"]').val(thismember.contact.address);
    $('input[name="city"]').val(thismember.contact.city);
    $('input[name="email"]').val(thismember.contact.email);
    $('.data-email-link').attr('href', 'mailto:'+thismember.contact.email).text(thismember.contact.email);
    $('#country').val(thismember.contact.country);
    $('#member-info').slideDown();
    $('input[name="username"]').val(thismember.account.username);
    $('select[name="theme"]').val(thismember.preferences.theme);
    $('select[name="language"]').val(thismember.preferences.language);
    var base_url = "/" + thismember.preferences.language + "/" + thismember.preferences.theme + '/member/edit/#/';
    $('#st-about').attr('href', base_url + thismember_id + '/about');
    $('#st-contact').attr('href', base_url + thismember_id + '/contact');
    $('#st-billing').attr('href', base_url + thismember_id + '/billing');
    $('#st-memberships').attr('href', base_url + thismember_id + '/memberships');
};

function act_on_route(id) {
    if (thismember_id != id) {
        select_member_box.hide();
        thismember_id = id;
        var params = {'member_id': id};
        jsonrpc('member.profile', params, on_member_profile, error);
        get_billing_preferences();
        get_billing_pref_details();
    };
};

//********************************Tabs******************************************
$("#profile_tabs").tabs({
    collapsible:false
});
//-------------------------------End Tabs---------------------------------------
function show_profile() { $("#profile_tabs").tabs('select', 0); };
function show_memberships() { $("#profile_tabs").tabs('select', 1); };
function show_billing() { $("#profile_tabs").tabs('select', 2); };
function show_usages() { $("#profile_tabs").tabs('select', 3); };
function show_invoices() { $("#profile_tabs").tabs('select', 4); };

function setup_routing () {

    var routes = {
        '/:id': {
            '/profile': show_profile,
            '/billing': show_billing,
            '/memberships': show_memberships,
            '/usages': show_usages,
            '/invoices': show_invoices,
            on: act_on_route
        },
    };

    Router(routes).use({ recurse: 'forward' }).init();
};

function on_result_click (data) {
    select_member_box.text("loading ...");
    thismember_id = data['attributes']['id'];
    var params = {'member_id': thismember_id};
    jsonrpc('member.profile', params, on_member_profile, error);
    select_member_box.hide();
    get_billing_preferences();
    get_billing_pref_details();
}; 

function autocomplete() {
    $('#member-search').autoSuggest("/search/members", {
        selectedItemProp: "name",
        selectedValuesProp: "id", 
        searchObjProps: "name, email, id",
        minChars: 1,
        selectionLimit: 0, 
        startText: "Enter name or email or id",
        resultClick: function (data) {
            var id = data['attributes']['id'];
            var basepath = window.location.pathname.split('/').slice(0,3).join('/');
            window.location = basepath + "/member/edit/#/" +id+ "/about";
        }
    });
};

setup_routing();
autocomplete();

function edit_member(theform) {
    var action_status = $('#'+theform.attr('id') + ' .action-status');
    var inputs = theform.serializeArray();
    var params = {'member_id': thismember_id}
    for(var i in inputs) {
        params[inputs[i].name] = inputs[i].value;
    };
    function success(resp) {
        action_status.text("Update is successful.").attr('class', 'status-success');
    };
    function error() {
        action_status.text("Update failed").attr('class', 'status-fail');
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
$("#billing_pref #mode").click(function(){
    $("#details_1").hide();
    $("#details_2").hide();
    $("#details_3").hide();
    mode = $(this).val();
    $("#details_"+mode).show();
});
$("#organization_mode0").click(function(){
    $('#details_3 #org_name').attr('disabled', 'disabled');
    $('#details_3 #org_address').attr('disabled', 'disabled');
    $('#details_3 #org_city').attr('disabled', 'disabled');
    $('#details_3 #org_country').attr('disabled', 'disabled');
    $('#details_3 #org_phone').attr('disabled', 'disabled');
    $('#details_3 #org_email').attr('disabled', 'disabled');
    $('#details_3 #existing_org').removeAttr('disabled');
});
$("#organization_mode1").click(function(){
    $('#details_3 #org_name').removeAttr('disabled');
    $('#details_3 #org_address').removeAttr('disabled');
    $('#details_3 #org_country').removeAttr('disabled');
    $('#details_3 #org_city').removeAttr('disabled');
    $('#details_3 #org_phone').removeAttr('disabled');
    $('#details_3 #org_email').removeAttr('disabled');
    $('#details_3 #existing_org').attr('disabled', 'disabled');
});

//---------------------Save Billing Preferences---------------------------------
$("#update-billingpref").click(function(){
    var params = {'member': thismember_id, 'mode': parseInt(mode)};
    switch(parseInt(mode)){
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
        case 3 : if(parseInt($("input:radio[name='organization_mode']:checked").val()) == 1){
                    params['org_details'] = {
                        "name" :$("#details_3 #org_name").val(),
                        "address" :$("#details_3 #org_address").val(),
                        "city" :$("#details_3 #org_city").val(),
                        "country" :$("#details_3 #org_country").val(),
                        "phone" :$("#details_3 #org_phone").val(),
                        "email" :$("#details_3 #org_email").val()
                        };
                 }
                 else{
                    params['billto'] = billto;
                 }
                 break;
    }
    function on_save_billingpref_success(){
        $("#billing_pref-msg").html("<big>☑</big> Billing Preferences Saved Successfully.");
        get_billing_pref_details();
    };
    function on_save_billingpref_error(){
        $("#billing_pref-msg").html("<big>Error in saving Billing Preferences. Try again</big>");
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
                     $('input:radio[name=organization_mode][value=0]').click();
                     break;
           case 2 : $('input:radio[name=mode][value=2]').click();
                    $('input:radio[name=organization_mode][value=0]').click();
                    break;
           case 3 : $('input:radio[name=mode][value=3]').click();
                    $('input:radio[name=organization_mode][value=0]').click();
                    break;
        }   
    };
    function on_get_billingpref_error(){};
    var params = {'member': thismember_id};
    jsonrpc('billingpref.info', params, on_get_billingpref_success, on_get_billingpref_error);
};
//-------------------------Get Billing Preferences Details----------------------
function get_billing_pref_details(){
    function on_success(resp){
        $('#billing_preferences_view_section #bill_name').text(resp['result']['name']);
        $('#billing_preferences_view_section #bill_address').text(resp['result']['address']);
        $('#billing_preferences_view_section #bill_city').text(resp['result']['city']);
        $('#billing_preferences_view_section #bill_country').text(resp['result']['country']);
        $('#billing_preferences_view_section #bill_phone').text(resp['result']['phone']);
        $('#billing_preferences_view_section #bill_email').text(resp['result']['email']);
    };
    function on_error(){};
    var args = {'member': thismember_id};
    jsonrpc('billingpref.details', args, on_success, on_error);
};
//------------------------Existing Member Search--------------------------------
$('#details_2 #member').autocomplete({
    source: "/search/members", 
    select: function (event, ui) {
        billto = ui.item.id;
    } 
});
//------------------------Existing Organization Search--------------------------
$('#details_1 #existing_org').autocomplete({
    source: "/search/organizations", 
    select: function (event, ui) {
        billto = ui.item.id;
    } 
});
//************************End of Billing Preferences****************************
// ***************************Next Tariff***************************************
 
$('#next-tariff-form #start-vis').datepicker( {
    altFormat: 'yy-mm-dd',
    altField: '#start',
    dateFormat: 'M d, yy'
});
$('#next_tariff-btn').click(function() {
    $('#next-tariff-form').dialog({ 
        title: "Next Tariff", 
        width: 500, 
        buttons: {
            "Save": function() { 
                var params = {}
                function success(resp) {
                    $(this).dialog("close"); 
                    window.location.reload();
                    $("#Next_Tariff-msg").html("");
                };
                function error() {
                    $("#Next_Tariff-msg").html("<big>Error in Assigning Tariff. Try again</big>");
                };
                params['member_id'] = thismember_id;
                params['tariff_id'] = $("#next-tariff-form #tariff").val();
                params['starts'] = to_iso_date($("#next-tariff-form #start").val());
                jsonrpc('tariff.new_member', params, success, error);
    
            }, 
            "Cancel": function() { 
                $(this).dialog("close"); 
                $("#Next_Tariff-msg").html("");
            }
        } 
    });
});

var params1 = {}
function success1(resp) {     
    $("#tariff-options").tmpl(resp['result']).appendTo( "#next-tariff-form #tariff" );
    $("#tariff-options").tmpl(resp['result']).appendTo( "#change-tariff-form #tariff" );
    };
function error1(){};
params1['bizplace_id'] = current_ctx;
jsonrpc('bizplace_tariffs.list', params1, success1, error1);
    
//*************************End Next Tariff**************************************

//**************************Tariff History**************************************
$('#load-tariff-history').click(function(){
   var params = {}
    function success2(response) {
        for(i in response.result){
            response.result[i].starts = to_formatted_date(response.result[i].starts);
        }
        $('#tariff-row').tmpl(response.result).appendTo('#tariff-info');
        $('#load-tariff-history').hide();
        bind_cancel_and_change_tariff();
        };
    function error2(){};
    params['member_id'] = thismember_id;
    jsonrpc('tariff.member_memberships', params, success2, error2); 
});
//***************************End Tariff History*********************************
//************************Cancel/Change Tariff**********************************
$('#change-tariff-form #starts-vis').datepicker( {
    altFormat: 'yy-mm-dd',
    altField: '#change-tariff-form #starts',
    dateFormat: 'M d, yy'
});
$('#change-tariff-form #ends-vis').datepicker( {
    altFormat: 'yy-mm-dd',
    altField: '#change-tariff-form #ends',
    dateFormat: 'M d, yy'
});

function bind_cancel_and_change_tariff() {
    $('.cancel-sub').click(function(){
        var params = {'membership_id': $(this).attr('id').split("-")[1]};
        function success(response) {
            $("#tariff_row-"+params['membership_id']).hide();     
        };
        function error(){};
        if(confirm("Do you want to remove?")){
            jsonrpc('membership.remove', params, success, error);
        }
    });
    $('.change-sub').click(function(){
        var membership_id = $(this).attr('id').split("-")[1];
        var date = iso_to_formatted($("#tariff_row-"+membership_id+" #starts").text());
        $('#change-tariff-form #starts-vis').datepicker("setDate", date);
        if($("#tariff_row-"+membership_id+" #ends").text()!="-"){
            date = iso_to_formatted($("#tariff_row-"+membership_id+" #ends").text());
            $('#change-tariff-form #ends-vis').datepicker("setDate", date);
        }
        $("#change-tariff-form #tariff option:contains('" + $("#tariff_row-"+membership_id+" #tariff_name").text() + "')").attr('selected', 'selected');
        $('#change-tariff-form').dialog({ 
            title: "Change Tariff", 
            width: 500, 
            buttons: {
                "Save": function() { 
                    var params = {'membership_id':membership_id};
                    params['tariff_id'] = $("#change-tariff-form #tariff").val();
                    params['tariff_name'] = $("#change-tariff-form #tariff option[value='"+params['tariff_id']+"']").text();
                    params['starts'] = to_iso_date($('#change-tariff-form #starts').val());
                    if($('#change-tariff-form #end').val() != ""){
                        params['ends'] = to_iso_date($('#change-tariff-form #ends').val());
                    }
                    function success(resp) { 
                        var date = to_formatted_date(params['starts']);
                        $("#tariff_row-"+membership_id+" #start").text(date);//$.datepicker.formatDate('M dd, yy', date));
                        date = to_formatted_date(params['ends']);
                        $("#tariff_row-"+membership_id+" #ends").text(date);//$.datepicker.formatDate('M dd, yy', date));
                        $("#tariff_row-"+membership_id+" #tariff_name").text($("#change-tariff-form #tariff option[value='"+params['tariff_id']+"']").text());
                        $("#Change_Tariff-msg").html("");
                        $('#change-tariff-form').dialog("close");
                    };
                    function error() {
                        $("#Change_Tariff-msg").html("<big>Error in Changing Tariff. Try again</big>");
                    };
                    jsonrpc('membership.change', params, success, error);
                }, 
                "Cancel": function() { 
                    $(this).dialog("close"); 
                    $("#Change_Tariff-msg").html("");
                }
            } 
        });
    });
};   
//***********************End Cancel/Change Tariff*******************************

