var checked_map = {'checked':true, 'on':true, undefined:false};
$("#add_tax-btn").click(function(){
    var data = {};
    data.name = $("#new_tax").val();
    data.value = $("#new_value").val();
    append_taxes([data]);
});
function append_taxes(data){
    $("#tax_tmpl").tmpl(data).appendTo("#taxes_list");
    $("#new_tax").val("");
    $("#new_value").val("");
    $(".remove-tax").unbind('click');
    $(".remove-tax").click(function(){
        $(this).parent().remove();
    });
}
$(".remove-tax").click(function(){
    $(this).parent().remove();
});
$("#taxation").submit(function(){
    $(this).checkValidity();
    update_taxes();
    return false;
});
$(".step-controls").hide();
function update_taxes(){
    params = {'owner' : current_ctx};
    params.tax_included = checked_map[$("#taxes_included:checked").val()];
    params.taxes = null;
    $('.new-tax').each(function(){
        params.taxes = {};
        params.taxes[$(".new-name", this).val()] = $(".new-value", this).val();
    });
    function on_taxes_updation_success(){
        $(".action-status").removeClass('status-fail');
        $(".action-status").text("Taxes saved successfully.").attr('class', 'status-success');
    };
    function on_taxes_updation_error(){
        $(".action-status").removeClass('status-success');
        $(".action-status").text("Error in saving taxes.").attr('class', 'status-fail');
    };
    jsonrpc("invoicepref.update", params, on_taxes_updation_success, on_taxes_updation_error);  
};
function get_taxesinfo(){
    function on_get_taxinfo_success(resp){
        $("#taxes_included").attr("checked", resp.result.tax_included);
        var taxes = resp.result.taxes;
        for(var key in taxes){
            append_taxes([{'name':key, 'value':taxes[key]}]);
        };
    };
    jsonrpc("invoicepref.taxinfo", {"owner":current_ctx}, on_get_taxinfo_success);
};
get_taxesinfo();
