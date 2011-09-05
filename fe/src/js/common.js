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
//******************************Load List of Bizplaces**************************************************
    function success(resp){
        if(resp['result'].length == 0)
            $("#bizplaces").hide();
        else
        {
            $("#bizplaces").show();
            for(bizplace in resp['result'])
                $("#bizplaces").append("<option value="+resp['result'][bizplace]['bizplace_id']+">"+resp['result'][bizplace]['bizplace_name']+"</option>");
            if($.cookie("bizplace"))
                jQuery("#bizplaces option[value='"+$.cookie("bizplace")+"']").attr('selected', 'selected');
            else
                $.cookie("bizplace", $("#bizplaces").find('option:selected').val());
        }
        $('#bizplaces').change(function(){
	        var val = $("#bizplaces").find('option:selected').val();
	        $.cookie("bizplace", val);
	        window.location.reload();
	    });
    }
    function error(){
    }
    params = {'user_id':$.cookie('user_id'), 'role_filter':['director','host']};
    if(params['user_id'])
        jsonrpc('users.bizplace.list', params, success, error); 
     
//******************************************End**********************************************************
  
$(document).ready(function() {
    init_autocomplete();
    init_nav();
});    

