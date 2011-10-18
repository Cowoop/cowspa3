// Globals
current_ctx = parseInt($.cookie("current_ctx"));
//

$.webshims.setOptions('forms', {
    overrideMessages: true
});

//load all polyfill features
//or load only a specific feature with $.webshims.polyfill('feature-name');
$.webshims.polyfill();

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
            id = data['attributes']['id'];
            path = $("#navlink-aboutme").attr('href');
            path = path.substring(0,path.indexOf("profile"))
            window.location = path+"profile?id="+id+"#about";
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
        // $('#submenu_' + m_id).show();
        $(this).addClass('current');
        var submenu = $('#submenu_' + m_id);
        if(submenu) {
            $('#submenu_' + m_id).slideDown('fast');
            $('#main .content').addClass('opaq');
            $('nav').addClass('simple-box');
        };
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
    } else {
        $('#context-opt-tmpl').tmpl(resp.result).appendTo('#context-select');
        if (current_ctx) {
            $("#context-select option[value='" + current_ctx + "']").attr('selected', 'selected');
        };
        $('#context-select').change(function() {
            set_context($('#context-select').find('option:selected').val());
        });
        set_context($("#context-select").find('option:selected').val());
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
