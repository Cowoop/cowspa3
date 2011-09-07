$(document).ready(function() {
    var result;
    
    var hash = window.location.hash;
    if(hash == "#account")
        $("#account_edit_form").show();
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
        result = response;
    };
    function error() {
    };
    if(window.location.search)
    {
        profile_id = (window.location.search).substring(4);
        path = window.location.pathname+window.location.search;
        $(".navlink-opt-item").each(function () {
            $(this).attr('href', path + '#' + $(this).attr('href').split('#')[1]);
        });
        $("#navlink-aboutme").text("About");
        $("#navlink-social").text("Social");
    }
    else
        profile_id = $.cookie('user_id');
    params = {'member_id': profile_id};
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
        result['result']['preferences'] = save("preferences", "member.update", params);
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
//*********************Next Teriff**********************************
     
    $('#next-tariff-form #start').datepicker({
        dateFormat: 'dd.mm.yy',
    });
    $('#next_tariff-btn').click(function() {
        $('#next-tariff-form').dialog({ 
            title: "Next Tariff", 
            width: 500, 
            buttons: {
                "Save": function() { 
                    var params = {}
                    function success(resp) {
                    };
                    function error() {
                    };
                    params['subscriber_id'] = $.cookie('user_id');
                    params['plan_id'] = $("#next-tariff-form #tariff").val();
                    params['starts'] = $("#next-tariff-form #start").val();
                    jsonrpc('next.tariff', params, success, error);
                    $(this).dialog("close"); 
                    }, 
                "Cancel": function() { 
                    $(this).dialog("close"); 
                    }
                } 
        });
    });
   
    var params = {}
    function success1(resp) {     
        $("#tariff-options").tmpl(resp['result']).appendTo( "#next-tariff-form #tariff" );
        };
    function error1() {
        };
    params['bizplace_id'] = $("#bizplaces").val();
    jsonrpc('bizplace_plans.list', params, success1, error1);
    
    
//*******************End Modal Window**************************
});
