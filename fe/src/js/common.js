$.jsonRPC.setup({
    endPoint: '/app',
    namespace: ''
});

function jsonrpc(apiname, params, success, error) {
    $.jsonRPC.request(apiname, {
        params: params,
        success: success,
        error: error
    });
};

function init_autocomplete() {
    $('input#search').autoSuggest("/search_members", {
        selectedItemProp: "name",
        selectedValuesProp: "id", 
        searchObjProps: "name, email, id",
        minChars: 1,
        selectionLimit: 0, 
        startText: "Enter name or email or id",
        /*
        formatList: function(item){ 
            return ("<li>"+"<div class='display_name'>"+item.name+" (ID:"+ item.id+")</div><div class='email'>"+item.email+"</div></div></li>");
        },*/
        resultClick: function (data) {
            id = data['attributes']['id'];
            path = $("#navlink-aboutme").attr('href');
            path = path.substring(0,path.indexOf("profile"))
            window.location = path+"profile?id="+id+"#about";
        } 
    });
};

function init_nav() {
    function set_current_opt () {
        $('.nav-opt-item a').each( function () {
            if ($(this).attr('href') == (window.location.pathname + window.location.hash)) {
                $(this).parent().addClass('nav-opt-item-current');
            };
        });
    };
    $('nav h2').click( function () {
        $('nav div.nav-opt').removeClass('open');
        $('nav h2').removeClass('nav-current');
        $(this).next().addClass('open').slideDown('slow');
        $('nav div.nav-opt:not(.open)').slideUp('fast');
        $(this).addClass('nav-current');
        $('.nav-opt-item').removeClass('nav-opt-item-current');
        set_current_opt();
    });
    $('nav div.nav-opt a').click( function () {
        $('.nav-opt-item').removeClass('nav-opt-item-current');
        $(this).parent().addClass('nav-opt-item-current');
    });
    set_current_opt();
};

  
$(document).ready(function() {
    init_autocomplete();
    init_nav();
});    

