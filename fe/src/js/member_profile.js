$(document).ready(function() {
    var result;
    
    var hash = window.location.hash;
    if(hash == "#account")
        $("#account_edit_form").show();
    else if(hash == "#billingpreferences")
        $("#billing_preferences_view_section").show();
    else
        $(hash+"_view_form").show();
    function success(response) {
        bind_values(response['result']['profile'], "about");
        bind_values(response['result']['profile'], "social");
        bind_values(response['result']['contact'], "contact");
        bind_values(response['result']['account'], "account");
        bind_values(response['result']['preferences'], "preferences");
        var first_name = response['result']['profile']['first_name'] || '';
        var last_name = response['result']['profile']['last_name'] || '';
        if (first_name || last_name) {
            var display_name = first_name + ' ' + last_name;
            $('.content .content-title').text(display_name);
        };
        $('#tariff-row').tmpl(response.result.memberships).appendTo('#tariff-info');
        bind_cancel_and_change_tariff();
        result = response;
    };
    function error() {
    };
    if(window.location.search)
    {
        profile_id = (window.location.search).substring(4);
        path = window.location.pathname+window.location.search;
        submenu = ['navlink-aboutme', 'navlink-memberships', 'navlink-account', 'navlink-contact', 'navlink-social', 'navlink-preferences', 'navlink-billingpreferences'];
        for(sub in submenu)
        {
            if($("#"+submenu[sub]).attr('href'))
                $("#"+submenu[sub]).attr('href', path + '#' + $("#"+submenu[sub]).attr('href').split('#')[1]);
        }
        $("#navlink-aboutme").text("About");
        $("#navlink-social").text("Social");
    }
    else
        profile_id = $.cookie('user_id');
    var params = {'member_id': profile_id};
    jsonrpc('member.profile', params, success, error);
    
    $('#about_edit_form #save-btn').click(function(){
        var params = { 'member_id' : profile_id};
        result['result']['profile'] = save("about", "member.update", params);
        });
    $('#about_view_form #edit-link').click(function(){
        edit("about");
        });
    $('#account_edit_form #save-btn').click(function(){
        var params = { 'member_id' : profile_id};
        result['result']['profile'] = save("account", "member.update", params);
        });
    $('#social_edit_form #save-btn').click(function(){
        var params = { 'member_id' : profile_id};
        result['result']['profile'] = save("social", "member.update", params);
        });
    $('#social_view_form #edit-link').click(function(){
        edit("social");
        })
    $("#contact_edit_form #save-btn").click(function(){
        var params = { 'member_id' : profile_id};
        result['result']['contact'] = save("contact", "member.update", params);
        });
    $("#contact_view_form #edit-link").click(function(){
        edit("contact");
        });
    $("#preferences_edit_form #save-btn").click(function(){
        var params = { 'member_id' : profile_id};
        var prev_theme = "/"+result['result']['preferences']['theme'].toLowerCase()+"/";
        result['result']['preferences'] = save("preferences", "member.update", params);
        var new_theme = "/"+result['result']['preferences']['theme'].toLowerCase()+"/";
        var location = window.location.toString();
        if(prev_theme != new_theme)
            window.location = location.replace(prev_theme, new_theme);
        });
    $("#preferences_view_form #edit-link").click(function(){
        edit("preferences");
        });
    
    $("#navlink-aboutme").click(function(){
        $('.profile-forms').each( function () {
            if ($(this).attr('id') == "about_view_form") 
                $(this).show();
            else
                $(this).hide();
            });
        });
    $("#navlink-account").click(function(){
        $('.profile-forms').each( function () {
            if ($(this).attr('id') == "account_edit_form") 
                $(this).show();
            else
                $(this).hide();
            });
        });
    $("#navlink-contact").click(function(){
        $('.profile-forms').each( function () {
            if ($(this).attr('id') == "contact_view_form") 
                $(this).show();
            else
                $(this).hide();
            });;
        });
    $("#navlink-social").click(function(){
        $('.profile-forms').each( function () {
            if ($(this).attr('id') == "social_view_form") 
                $(this).show();
            else
                $(this).hide();
            });
        });
    $("#navlink-memberships").click( function() {
        $('.profile-forms').hide();
        $('.profile-forms#memberships_view_form').show();
    });
    $("#navlink-preferences").click(function(){
        $('.profile-forms').each( function () {
            if ($(this).attr('id') == "preferences_view_form") 
                $(this).show();
            else
                $(this).hide();
            });
        });
    $("#navlink-billingpreferences").click(function(){
        $('.profile-forms').each( function () {
            if ($(this).attr('id') == "billing_preferences_view_section") 
                $(this).show();
            else
                $(this).hide();
            });
        });
    $(".topbar #theme").click(function(){
        $('.profile-forms').each( function () {
            if ($(this).attr('id') == "preferences_view_form") 
                $(this).show();
            else
                $(this).hide();
            });
        });
    $(".topbar #account").click(function(){
        $('.profile-forms').each( function () {
            if ($(this).attr('id') == "account_edit_form") 
                $(this).show();
            else
                $(this).hide();
            });
        });
    $('#about_edit_form #cancel-btn').click(function(){
        $("#about_edit_form").hide();
        bind_values(result['result']['profile'], "about");
        $("#about_view_form").show();
        });
    $("#contact_edit_form #cancel-btn").click(function(){
        $("#contact_edit_form").hide();
        bind_values(result['result']['contact'], "contact");
        $("#contact_view_form").show();
        });     
    $("#social_edit_form #cancel-btn").click(function(){
        $("#social_edit_form").hide();
        bind_values(result['result']['profile'], "social");
        $("#social_view_form").show();
        });
    $("#preferences_edit_form #cancel-btn").click(function(){
        $("#preferences_edit_form").hide();
        bind_values(result['result']['preferences'], "preferences");
        $("#preferences_view_form").show();
        });
//*********************Next Tariff**********************************
     
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
                    params['subscriber_id'] = $.cookie('user_id');
                    params['plan_id'] = $("#next-tariff-form #tariff").val();
                    params['starts'] = $("#next-tariff-form #start").val();
                    jsonrpc('next.tariff', params, success, error);
        
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
    params1['bizplace_id'] = $("#bizplaces").val();
    jsonrpc('bizplace_plans.list', params1, success1, error1);
    
    
//*******************End Next Tariff**************************

//***********************Tariff History**************************************
$('#load-tariff-history').click(function(){
   var params = {}
    function success2(response) {     
        $('#tariff-row').tmpl(response.result).appendTo('#tariff-info');
        $('#load-tariff-history').hide();
        bind_cancel_and_change_tariff();
        };
    function error2(){};
    params['member_id'] = $.cookie('user_id');
    jsonrpc('teriff.history', params, success2, error2); 
});
//************************End Tariff History*********************************
});
//************************Cancel/Change Tariff**********************************
function bind_cancel_and_change_tariff() {
    $('.cancel-sub').click(function(){
        var params = {'subscription_id': $(this).attr('id').split("-")[1]};
        function success(response) {
            $("#tariff_row-"+params['subscription_id']).hide();     
        };
        function error(){};
        if(confirm("Do you want to remove?")){
            jsonrpc('subscription.remove', params, success, error);
        }
    });
    $('.change-sub').click(function(){
        var subscription_id = $(this).attr('id').split("-")[1];
        var date = new Date($("#tariff_row-"+subscription_id+" #starts").text());
        date = $.datepicker.formatDate('mm/dd/yy', date);
        $('#change-tariff-form #start').val(date);
        if($("#tariff_row-"+subscription_id+" #ends").text()!="-"){
            date = new Date($("#tariff_row-"+subscription_id+" #ends").text());
            date = $.datepicker.formatDate('mm/dd/yy', date);
            $('#change-tariff-form #end').val(date);
        }
        $("#change-tariff-form #tariff option:contains('" + $("#tariff_row-"+subscription_id+" #plan_name").text() + "')").attr('selected', 'selected');
        $('#change-tariff-form').dialog({ 
            title: "Change Tariff", 
            width: 500, 
            buttons: {
                "Save": function() { 
                    var params = {'subscription_id':subscription_id};
                    params['plan_id'] = $("#change-tariff-form #tariff").val();
                    params['plan_name'] = $("#change-tariff-form #tariff option[value='"+params['plan_id']+"']").text();
                    params['starts'] = $('#change-tariff-form #start').val();
                    if($('#change-tariff-form #end').val() != ""){
                        params['ends'] = $('#change-tariff-form #end').val();
                    }
                    function success(resp) { 
                        $("#tariff_row-"+subscription_id+" #start").text(params['starts']);
                        $("#tariff_row-"+subscription_id+" #ends").text(params['ends']);
                        $("#tariff_row-"+subscription_id+" #plan_name").text($("#change-tariff-form #tariff option[value='"+params['plan_id']+"']").text());
                        $("#Change_Tariff-msg").html("");
                        $('#change-tariff-form').dialog("close");
                    };
                    function error() {
                        $("#Change_Tariff-msg").html("<big>Error in Changing Tariff. Try again</big>");
                    };
                    jsonrpc('subscription.change', params, success, error);
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

//*************************Billing Preferences**********************************
var mode, billto, details;
$("#billing_pref #mode").click(function(){
    $("#details_1").hide();
    $("#details_2").hide();
    $("#details_3").hide();
    mode = $(this).val();
    $("#details_"+mode).show();
});
$("#bizness_mode0").click(function(){
    $('#details_3 #biz_name').attr('disabled', 'disabled');
    $('#details_3 #biz_address').attr('disabled', 'disabled');
    $('#details_3 #biz_city').attr('disabled', 'disabled');
    $('#details_3 #biz_country').attr('disabled', 'disabled');
    $('#details_3 #biz_phone').attr('disabled', 'disabled');
    $('#details_3 #biz_email').attr('disabled', 'disabled');
    $('#details_3 #existing_biz').removeAttr('disabled');
});
$("#bizness_mode1").click(function(){
    $('#details_3 #biz_name').removeAttr('disabled');
    $('#details_3 #biz_address').removeAttr('disabled');
    $('#details_3 #biz_country').removeAttr('disabled');
    $('#details_3 #biz_city').removeAttr('disabled');
    $('#details_3 #biz_phone').removeAttr('disabled');
    $('#details_3 #biz_email').removeAttr('disabled');
    $('#details_3 #existing_biz').attr('disabled', 'disabled');
});
$('#billing_preferences_view_section #edit-link').click(function(){
    $('#billing_preferences_view_section').hide();
    $('#billing_preferences_edit_section').show();
    $("#billing_pref-msg").html("");
});
$('#billing_preferences_edit_section #cancel-billingpref').click(function(){
    $('#billing_preferences_edit_section').hide();
    $('#billing_preferences_view_section').show();
});
//---------------------Save Billing Preferences---------------------------------
$("#save-billingpref").click(function(){
    var params = {'member': (window.location.search ? (window.location.search).substring(4) : $.cookie('user_id')), 'mode': parseInt(mode)};
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
        case 3 : if(parseInt($("input:radio[name='bizness_mode']:checked").val()) == 1){
                    params['biz_details'] = {
                        "name" :$("#details_3 #biz_name").val(),
                        "address" :$("#details_3 #biz_address").val(),
                        "city" :$("#details_3 #biz_city").val(),
                        "country" :$("#details_3 #biz_country").val(),
                        "phone" :$("#details_3 #biz_phone").val(),
                        "email" :$("#details_3 #biz_email").val()
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
        $('#billing_preferences_edit_section').hide();
        $('#billing_preferences_view_section').show();
    };
    function on_save_billingpref_error(){
        $("#billing_pref-msg").html("<big>Error in saving Billing Preferences. Try again</big>");
    };
    jsonrpc('billingpref.update', params, on_save_billingpref_success, on_save_billingpref_error);
});
//------------------Get Billing Preferences-------------------------------------
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
                 $('input:radio[name=bizness_mode][value=0]').click();
                 break;
        case 2 : $('input:radio[name=mode][value=2]').click();
                 $('input:radio[name=bizness_mode][value=0]').click();
                 break;
        case 3 : $('input:radio[name=mode][value=3]').click();
                 $('input:radio[name=bizness_mode][value=0]').click();
                 break;
    }
};
function on_get_billingpref_error(){};
var params = {'member': (window.location.search ? (window.location.search).substring(4) : $.cookie('user_id'))};
jsonrpc('billingpref.info', params, on_get_billingpref_success, on_get_billingpref_error);
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
    var args = {'member': (window.location.search ? (window.location.search).substring(4) : $.cookie('user_id'))};
    jsonrpc('billingpref.details', args, on_success, on_error);
};
get_billing_pref_details();
//------------------------Existing Member Search--------------------------------
$('#details_2 #member').autocomplete({
    source: "/search/members", 
    select: function (event, ui) {
        billto = ui.item.id;
    } 
});
//------------------------Existing Biznesses Search--------------------------------
$('#details_1 #existing_biz').autocomplete({
    source: "/search/businesses", 
    select: function (event, ui) {
        billto = ui.item.id;
    } 
});
//************************End of Billing Preferences****************************
