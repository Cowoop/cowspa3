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
    $('.ctx-opt').removeClass('current-ctx');
    $('#ctx_' + ctx).addClass('current-ctx');
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

function hide_submenu() {
    $('.submenu-box').hide();
    $('#main .content').removeClass('opaq');
    $('nav').removeClass('simple-box');
    $('#main .content').addClass('simple-box');
};

function init_nav() {
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
            $('.submenu-container').addClass('simple-box');
        };
    });
    $('.submenu-item').click( function() {
        hide_submenu();
    });
    $('#main .content').addClass('simple-box');
};
//******************************Load List of Bizplaces**************************************************

function set_0_locations_menu() {
    $("#context-select").hide();
    $("#context-single").hide();
    $('#menu-item_2').hide();
    $('#menu-item_3').hide();
    $('#menu-item_4').hide();
    set_context(null);
};

function hide_ctx_menu() {
    $('#main .content').removeClass('opaq');
    $('#ctx-menu').slideUp();
    $('#ctx-switcher').removeClass('open');
    // $('#ctx-switcher-title').removeClass('open');
    $('#main .content').addClass('simple-box');
};

function toggle_ctx_menu() {
    $('#main .content').toggleClass('opaq');
    $('#ctx-menu').slideToggle();
    $('#ctx-switcher').toggleClass('open');
    // $('#ctx-switcher-title').toggleClass('open');
    $('#main .content').toggleClass('simple-box');
};

function on_roles_list(resp) {
    var result = resp.result;
    $(document).ready( function() {
        on_roles(result)
    }); // calling on_roles hook which might be defined (only once) at some other js

    var ctx_label = 'Location options';
    if(result.length == 0) {
        $('#ctx-menu').show();
        set_0_locations_menu();
    }
    else if(result.length == 1) {
        ctx_label = result[0].label;
        $('#ctx-tmpl').tmpl(result).appendTo('#ctx-opts');
        set_context(result[0].id);
    }
    else {
        $('#ctx-tmpl').tmpl(result).appendTo('#ctx-opts');
        if (current_ctx) {
            var valid_bizplaces = [];
            for (idx in result) { valid_bizplaces.push(result[idx].id); };
            if (valid_bizplaces.indexOf(current_ctx) == -1) {
                var ctx = (valid_bizplaces.length == 0? null: valid_bizplaces[0]);
                set_context(ctx);
            };
            for (idx in result) {
                if (result[idx].id == current_ctx) {
                    ctx_label = result[idx].label;
                    break;
                };
            }; 
        } else {
            ctx_label = result[0].label;
            set_context(result[0].id);
        };
    };
    $('#ctx-switcher-title').text(ctx_label + " ▼");
    $('#ctx-switcher-title').click( function () {
        toggle_ctx_menu();
    });
    $('.ctx-opt').click( function () {
        var ctx_id = $(this).attr('id').split('_')[1];
        set_context(ctx_id);
        toggle_ctx_menu();
        window.location.reload();
    });
};

$(document).click( function (e) {
    var t = $(e.target);
    var p = $(e.target).parent()
    if (!( t.hasClass('ctx-title') | p.hasClass('menu-item') | p.hasClass('submenu-item'))) {
        hide_ctx_menu();
        hide_submenu();
    };
});

function on_roles(roles) {}; // HOOK

function error(){ };

// TODO : Update role_filter when additional roles like accountant are added

params = {'user_id':$.cookie('user_id'), 'role_filter':['director','host']};
if(params['user_id']) {
    jsonrpc('roles.list', params, on_roles_list, error); 
};
     
//******************************************End**********************************************************
//*******************************************Date Formatting*********************************************
function iso2date(iso) {
    var yy = parseInt(iso.slice(0, 4));
    var mm = parseInt(iso.slice(5, 7)-1);
    var dd = parseInt(iso.slice(8, 10));
    var hh = parseInt(iso.slice(11, 13));
    var mi = parseInt(iso.slice(14, 16));
    var ss = parseInt(iso.slice(17, 19));
    var dt = new Date(yy, mm, dd, hh, mi, ss);
    return dt;
};

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
