// Globals
var current_ctx = $.cookie("current_ctx")?parseInt($.cookie("current_ctx"), 10):null;
var current_userid = parseInt($.cookie("user_id"), 10);
var current_role = window.location.pathname.split('/').slice(2,3)[0];
var member_name = $.cookie("member_name");
var basepath = window.location.pathname.split('/').slice(0,4).join('/');
var locale_data = {
                    currency_symbol:'$',
                    decimal_sep:'.',
                    group_sep:','
                 }; //default values
var fdate_format = "MMM D, YYYY";
var ftime_format = "hh:mm A";
var fdatetime_format = fdate_format + ' ' + ftime_format;
var allow_async = false;
function error() {};
//

$.webshims.setOptions('forms', {
    overrideMessages: true
});

//load all polyfill features
//or load only a specific feature with $.webshims.polyfill('feature-name');
$.webshims.polyfill();// forms-ext');

// extending jq
jQuery.fn.reset = function () {
    $(this).each (function() { this.reset(); });
};

// Cookies
var cookie_opts = { path : '/'};
function set_cookie(cookie_name, value) {
    return $.cookie(cookie_name, value, cookie_opts);
};
function delete_cookie(cookie_name) {
    return $.cookie(cookie_name, null, cookie_opts);
};
function format_currency(num) {
    return accounting.formatMoney(num, {
        symbol: locale_data.currency_symbol,
        thousand: locale_data.group_sep,
        decimal:locale_data.decimal_sep
    });
};
//

$.jsonRPC.setup({
    endPoint: '/app',
    namespace: ''
});

function set_locale(ctx) {
    function success(resp) {
        locale_data.currency_symbol = resp.result.symbol;
        locale_data.decimal_sep = resp.result.decimal;
        locale_data.group_sep = resp.result.group;
        allow_async = true;
    };
    var params = {'bizplace_id': ctx, 'user_id': current_userid};
    jsonrpc('bizplace.currency', params, success, error);
};

function set_context(ctx) {
    current_ctx = ctx;
    if (ctx == null) {
        delete_cookie("current_ctx");
    } else {
        var params = {'bizplace_id': ctx, 'user_id': current_userid};
        set_cookie("current_ctx", ctx);
        $('.ctx-opt').removeClass('current-ctx');
        $('#ctx_' + ctx).addClass('current-ctx');
    };
};

function set_userid(uid) {
    current_userid = uid;
    set_cookie("user_id", uid);
};

function jsonrpc(apiname, params, success, error, async) {
    var waiting_ele = $('div#main');
    waiting_ele.addClass('waiting');
    if (typeof(async) === 'undefined') { async = allow_async; };
    if (typeof(error) === 'undefined') { error = function(resp) { alert('Remote error: ' + apiname + ': ' + resp.error.message); }; };
    var cs_success = function(args) {
        waiting_ele.removeClass('waiting');
        success(args);
    };
    var cs_error = function(args) {
        waiting_ele.removeClass('waiting');
        error(args);
    };
    $.jsonRPC.request(apiname, {
        params: params,
        success: cs_success,
        error: cs_error,
        async: async
    });
};

function init_autocomplete() {
    $('input#search').autoSuggest("/search/member", {
        selectedItemProp: "name",
        selectedValuesProp: "id",
        searchObjProps: "name, email, id",
        minChars: 2,
        selectionLimit: 0,
        extraParams: '&context=' + current_ctx,
        startText: "Search member",
        resultClick: function (data) {
            var id = data['attributes']['id'];
            window.location = basepath + "/member/edit/#/" +id+ "/info";
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

function check_page_access(roles) {
    var allow_access = false;
    for (var i=0; i<roles.length; i++) {
        if (roles[i].context == current_ctx) {
            var ctx_roles = roles[i].roles;
            $.each(ctx_roles, function(idx, role) {
                if (role.role == current_role) {
                    allow_access = true;
                };
            });
            if (allow_access) {
                break;
            };
        };
    };
    if (!allow_access) {
        window.location = "/";
    };
};

function on_roles_list(resp) {
    var result = resp.result;
    $(document).ready( function() {
        on_roles(result)
    }); // calling on_roles hook which might be defined (only once) at some other js

    var ctx_label = 'Options';
    if(result.length == 0) {
        $('#ctx-menu').show();
        set_0_locations_menu();
    }
    else if(result.length == 1) {
        ctx_label = result[0].label;
        $('#ctx-tmpl').tmpl(result).appendTo('#ctx-opts');
        set_context(result[0].context);
        set_locale(current_ctx);
    }
    else {
        $('#ctx-tmpl').tmpl(result).appendTo('#ctx-opts');
        if (current_ctx) {
            var valid_bizplaces = [];
            for (var idx=0; idx < result.length; idx++) { valid_bizplaces.push(result[idx].context); };
            if (valid_bizplaces.indexOf(current_ctx) == -1) {
                var ctx = (valid_bizplaces.length == 0? null: valid_bizplaces[0]);
                set_context(ctx);
            };
            for (var idx=0; idx < result.length; idx++) {
                if (result[idx].context == current_ctx) {
                    ctx_label = result[idx].label;
                    set_context(current_ctx);
                    break;
                };
            }; 
        } else {
            ctx_label = result[0].label;
            set_context(result[0].context);
        };
        if(current_ctx) {
            set_locale(current_ctx);
        };
    };
    check_page_access(result);
    $('#ctx-switcher-title').text(ctx_label + " ▼");
    $('#ctx-switcher-title').click( function () {
        toggle_ctx_menu();
    });
    $('.ctx-opt').click( function () {
        var ctx_id = parseInt($(this).attr('id').split('_')[1], 10);
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

     
//******************************************End**********************************************************
//*******************************************Date Formatting*********************************************

var iso_date_format = "YYYY-MM-DD"; // momentjs only
var iso_format = iso_date_format + "\THH:mm:ss"; // momentjs only

function iso2date(iso){
    var yy = parseInt(iso.slice(0, 4), 10);
    var mm = parseInt(iso.slice(5, 7)-1, 10);
    var dd = parseInt(iso.slice(8, 10), 10);

    if (iso.length > 11) { // this won't work after year 9999 or before year 1000
        var hh = parseInt(iso.slice(11, 13), 10);
        var mi = parseInt(iso.slice(14, 16), 10);
        var ss = parseInt(iso.slice(17, 19), 10);

    } else {
        var hh = 0;
        var mi = 0;
        var ss = 0;
    };

    var dt = new Date(yy, mm, dd, hh, mi, ss);
    return dt;
};

function date2isotime(date, exclude_sec){
    if(jQuery.trim(date) == ""){
        return null;
    };
    var hh = date.getHours();
    hh = (hh<10?"0":"") + hh; 
    var mm = date.getMinutes();
    mm = (mm<10?"0":"") + mm;
    var ss = date.getSeconds();
    ss = (ss<10?"0":"") + ss;
    return (exclude_sec) ? hh+':'+mm : hh+":"+mm+":"+ss;
};

function date2iso(date){
    if(jQuery.trim(date) == ""){
        return null;
    };
    return moment(date).format("YYYY-MM-DD") + 'T' + date2isotime(date);
};

function date2isodate(date){
    if(jQuery.trim(date) == ""){
        return null;
    };
    return moment(date).format("YYYY-MM-DD");
};

function fdate2datetime(fdate){
    if(jQuery.trim(fdate) == ""){
        return "";
    };
    return moment(fdate, fdatetime_format).toDate();
};

function fdate2date(fdate){
    if(jQuery.trim(fdate) == ""){
        return "";
    };
    return moment(fdate, fdate_format).toDate();
};

function fdate2iso(fdate){
    if(jQuery.trim(fdate) == ""){
        return null;
    };
    return moment(fdate, fdatetime_format).format(iso_format);
};
function fdate2isodate(fdate){
    if(jQuery.trim(fdate) == ""){
        return null;
    };
    return moment(fdate, fdate_format).format(iso_date_format);
};
function fdate2isotime(fdate){
    if(jQuery.trim(fdate) == ""){
        return null;
    };
    return moment(fdate, ftime_format).format("HH:mm:ss");
};

function iso2fdate(iso){
    if(iso==null || iso==""){
        return "";
    };
    return moment(iso, iso_format).format(fdatetime_format);
};

function iso2ftime(iso){
    if(iso==null || iso==""){
        return "";
    };
    return moment(iso, iso_format).format(ftime_format);
};

function isotime2fdate(iso){
    if(iso==null || iso==""){
        return "";
    };
    return moment(iso, "HH:mm:ss").format(ftime_format);
};

function isodate2fdate(iso){
    if(iso==null || iso==""){
        return "";
    };
    return moment(iso, iso_date_format).format(fdate_format);
};

function date2ftime(date) {
    var iso = date2iso(date);    
    return moment(iso, iso_date_format).format(ftime_format);
};

function get_week_range(adate, start) {
    // http://stackoverflow.com/a/8381494/84513
    start = start || 0;
    var day = adate.getDay() - start;
    var date = adate.getDate() - day;

    var start = new Date(adate.setDate(date));
    var end = new Date(adate.setDate(date + 6));
    return [start, end];
};

function set_member_name(name) {
    set_cookie('member_name', name);
    set_cookie("member_name", $.cookie("member_name").replace(/"/g, ""));
    member_name = name;
    var profile_link = $('#profile_link');
    if (profile_link) {
        profile_link.text(member_name);
        profile_link.attr('href', basepath + "/member/edit/#/" +current_userid+ "/profile");
    };
};
