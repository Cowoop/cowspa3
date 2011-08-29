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
    $('input#search').tokenInput("/search_members",{ 
        animateDropdown:false, 
        resultsFormatter: function(item){ 
            return ("<li>"+"<div class='display_name'>"+item.name+" (ID:"+ item.id+")</div><div class='email'>"+item.email+"</div></div></li>");
        },
        searchDelay: 500,
        tokenLimit: 1,
        placeholder: 'search...',
        hintText: 'Enter Name or Email or ID',
        onAdd: function () {
                alert($('input#search').tokenInput("get")[0]['id']);
                $('input#search').tokenInput("clear");
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
