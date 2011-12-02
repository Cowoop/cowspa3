// Globals
var current_ctx = $.cookie("current_ctx")?parseInt($.cookie("current_ctx")):null;
var current_userid = parseInt($.cookie("user_id"));
var member_name = $.cookie("member_name");
var basepath = window.location.pathname.split('/').slice(0,3).join('/');
//

$.webshims.setOptions('forms', {
    overrideMessages: true
});

//load all polyfill features
//or load only a specific feature with $.webshims.polyfill('feature-name');
$.webshims.polyfill();// forms-ext');

// Cookies
var cookie_opts = { path : '/'};
function set_cookie(cookie_name, value) {
    return $.cookie(cookie_name, value, cookie_opts);
};
function delete_cookie(cookie_name) {
    return $.cookie(cookie_name, null, cookie_opts);
};
//

$.jsonRPC.setup({
    endPoint: '/app',
    namespace: ''
});

function set_context(ctx) {
    current_ctx = ctx;
    if (ctx == null) {
        delete_cookie("current_ctx");
    } else {
        set_cookie("current_ctx", ctx);
    };
};

function set_userid(uid) {
    current_userid = uid;
    set_cookie("user_id", uid);
};

function jsonrpc(apiname, params, success, error) {
    $.jsonRPC.request(apiname, {
        params: params,
        success: success,
        error: error
    });
};

function init_autocomplete() {
    $('input#search').autoSuggest("/search/member", {
        selectedItemProp: "name",
        selectedValuesProp: "id", 
        searchObjProps: "name, email, id",
        minChars: 1,
        selectionLimit: 0, 
        startText: "Search member by name, email or id",
        resultClick: function (data) {
            var id = data['attributes']['id'];
            window.location = basepath + "/member/edit/#/" +id+ "/profile";
        } 
    });
};

function init_nav() {
    function hide_submenu() {
        $('.submenu-box').hide();
        $('#main .content').removeClass('opaq');
        $('nav').removeClass('simple-box');
        $('#main .content').addClass('simple-box');
    };
    $('.menu-item').click( function () {
        $('#main .content').addClass('opaq');
        hide_submenu();
        $('.menu-item').removeClass('current');
        var m_id = $(this).attr('id').split('_')[1];
        $(this).addClass('current');
        var submenu = $('#submenu_' + m_id);
        if(submenu) {
            $('#submenu_' + m_id).slideDown('fast');
            $('#main .content').addClass('opaq');
            $('nav').addClass('simple-box');
        };
    });
    $('.submenu-item').click( function() {
        hide_submenu();
    });
    $(document).click( function (e) {
        var t = $(e.target).parent();
        if (!(t.hasClass('menu-item') | t.hasClass('submenu-item')) ) {
            hide_submenu();
        };
    });
    $('#main .content').addClass('simple-box');
};
//******************************Load List of Bizplaces**************************************************

function on_roles_list(resp) {
    var result = resp.result;
    $(document).ready( function() {
        on_roles(result)
    }); // calling on_roles hook which might be defined (only once) at some other js
    if(result.length == 0) {
        $("#context-select").hide();
        $("#context-single").hide();
        $('#menu-item_2').hide();
        $('#menu-item_3').hide();
        $('#menu-item_4').hide();
        set_context(null);
    } 
    else if(result.length == 1) {
        $("#context-select").hide();
        $("#context-single").text(resp.result[0].label);
        set_context(result[0].id);
    }
    else {
        $("#context-single").hide();
        $('#context-opt-tmpl').tmpl(result).appendTo('#context-select');
        if (current_ctx) {
            var valid_bizplaces = [];
            for (idx in result) {
                valid_bizplaces.push(result[idx].id);
            };
            if (valid_bizplaces.indexOf(current_ctx) == -1) {
                var ctx = (valid_bizplaces.length == 0? null: valid_bizplaces[0]);
                set_context(ctx);
            } else {
                $("#context-select").val(current_ctx);
            };
        } else {
            set_context($("#context-select").val());
        };

        $('#context-select').change(function() {
            set_context($('#context-select').val());
            window.location.reload();
        });
    };
};

function on_roles(roles) {}; // HOOK

function error(){ };

// TODO : Update role_filter when additional roles like accountant are added

params = {'user_id':$.cookie('user_id'), 'role_filter':['director','host']};
if(params['user_id']) {
    jsonrpc('roles.list', params, on_roles_list, error); 
};
     
//******************************************End**********************************************************
//*******************************************Date Formatting*********************************************
function to_iso_date(date){
    if(jQuery.trim(date) == ""){
        return null;
    }
    var fdate = new Date(date);
    return  $.datepicker.formatDate('yy-mm-dd', fdate);
}
function to_iso_datetime(date){
    if(jQuery.trim(date) == ""){
        return null;
    }
    var fdate = new Date(date);
    var hh = fdate.getHours();
    hh = (hh<10?"0":"") + hh; 
    var mm = fdate.getMinutes();
    mm = (mm<10?"0":"") + mm;
    var ss = fdate.getSeconds();
    ss = (ss<10?"0":"") + ss;
    return $.datepicker.formatDate('yy-mm-dd', fdate)+"T"+hh+":"+mm+":"+ss;
}
function to_formatted_date(date){
    if(date==null){
        return "";
    }
    var fdate = new Date(date);
    return $.datepicker.formatDate('M dd, yy', fdate);
}
function to_formatted_datetime(date){
    if(date==null){
        return "";
    }
    var fdate = new Date(date);
    var hh = fdate.getHours();
    var time = " AM";
    if(hh>=12){
        time = " PM";
        hh -= 12;
    }
    hh = (hh<10?"0":"") + hh; 
    var mm = fdate.getMinutes();
    mm = (mm<10?"0":"") + mm;
    //var ss = fdate.getSeconds();
    //ss = (ss<10?"0":"") + ss;
    time = hh + ":" +  mm + time
    return $.datepicker.formatDate('M dd, yy', fdate) + " " + time;
}
//*******************************************************************************************************
$(document).ready(function() {
    $("#profile_link").text(member_name);
    $("#profile_link").attr('href', basepath + "/member/edit/#/" +current_userid+ "/profile");
    init_autocomplete();
    init_nav();
});    
