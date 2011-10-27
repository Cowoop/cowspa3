// Globals
current_ctx = parseInt($.cookie("current_ctx"));
//

$.webshims.setOptions('forms', {
    overrideMessages: true
});

//load all polyfill features
//or load only a specific feature with $.webshims.polyfill('feature-name');
$.webshims.polyfill();// forms-ext');

$.jsonRPC.setup({
    endPoint: '/app',
    namespace: ''
});

function set_context(ctx) {
    current_ctx = ctx;
    $.cookie("current_ctx", ctx);
};

function jsonrpc(apiname, params, success, error) {
    $.jsonRPC.request(apiname, {
        params: params,
        success: success,
        error: error
    });
};

function init_autocomplete() {
    $('input#search').autoSuggest("/search/members", {
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

function success(resp) {
    if(resp['result'].length == 0) {
        $("#context-select").hide();
        $('#menu-item_3').hide();
        $('#menu-item_4').hide();
        $('#menu-item_5').hide();
    } else {
        $('#context-opt-tmpl').tmpl(resp.result).appendTo('#context-select');
        if (current_ctx) {
            $("#context-select").val(current_ctx);
        } else {
            set_context($("#context-select").val());
        };
        $('#context-select').change(function() {
            set_context($('#context-select').val());
        });
    };
};

function error(){ };

params = {'user_id':$.cookie('user_id'), 'role_filter':['director','host']};
if(params['user_id']) {
    jsonrpc('users.bizplace.list', params, success, error); 
};
     
//******************************************End**********************************************************
  
$(document).ready(function() {
    init_autocomplete();
    init_nav();
});    
