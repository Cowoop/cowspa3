$.jsonRPC.setup({
    endPoint: '/app',
    namespace: ''
});

function jsonrpc(apiname, params, success, error) {
    console.log($.jsonRPC.request(apiname, {
        params: params,
        success: success,
        error: error
    }))
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
    $('nav h2').click( function () {
        $('nav div.nav-opt').removeClass('open');
        $(this).next().addClass('open').slideDown('slow');
        $('nav div.nav-opt:not(.open)').slideUp('fast');
    } );
};

  
$(document).ready(function() {
    init_autocomplete();
    init_nav();
});    
