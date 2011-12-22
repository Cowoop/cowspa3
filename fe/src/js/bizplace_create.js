var theform = $('#bizplace_form');
var checked_map = {'checked':true, 'on':true, undefined:false};

function create_bizplace() {
    var action_status = $('#bizplace_form .action-status');
    var params = {};
    $('#bizplace_form .input').each(function(){
        if($(this).hasClass('taxes')==false){
            params[$(this).attr('name')] = $(this).val();
        };
    });
    params['tax_included'] = checked_map[$("#taxes_included:checked").val()];
    if(!params['tax_included']){
        params['default_taxes'] = {};
        $('.new-tax').each(function(){
            params['default_taxes'][$(".new-name", this).val()] = $(".new-value", this).val();
        });
    }
    function success() {
        action_status.text("Location created successfully").attr('class', 'status-success');
        window.location = basepath + '/dashboard';
    };
    function error() {
        action_status.text("Error in creating location").attr('class', 'status-fail');
    };
    jsonrpc('bizplace.new', params, success, error);
};

theform.submit( function () {
    $(this).checkValidity();
    create_bizplace();
    return false;
});

$("#add_tax-btn").click(function(){
    var data = {};
    data.name = $("#new_tax").val();
    data.value = $("#new_value").val();
    $("#tax_tmpl").tmpl([data]).appendTo("#taxes_list");
    $("#new_tax").val("");
    $("#new_value").val("");
    $(".remove-tax").unbind('click');
    $(".remove-tax").click(function(){
        $(this).parent().remove();
    });
});
$("#taxes_included").click(function(){
    if(checked_map[$("#taxes_included:checked").val()]){
        $("#taxes_list *").attr('disabled', 'disabled');
    } 
    else{
        $("#taxes_list *").removeAttr('disabled');
    }
});
$(".remove-tax").click(function(){
    $(this).parent().remove();
});
$("#taxes_included").attr("checked", true);
$("#taxes_list *").attr('disabled', 'disabled');
