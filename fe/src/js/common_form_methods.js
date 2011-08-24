function bind_values(values, form_name){
    for( var key in values)
    {
        if(['twitter', 'facebook', 'linkedin'].indexOf(key) != -1)
        {
            if(values[key])
            {
                $("#"+form_name+"_view_form #"+key).text(values[key][0]);
                $("#"+form_name+"_view_form #"+key).attr("href",values[key][1]); 
                $("#"+form_name+"_edit_form #"+key+"-label").val(values[key][0]);
                $("#"+form_name+"_edit_form #"+key+"-url").val(values[key][1]);
            }
        }
        else if(['website' ,'blog'].indexOf(key) != -1)
        {
            $("#"+form_name+"_view_form #"+key).text(values[key]);
            $("#"+form_name+"_view_form #"+key).attr("href",values[key]); 
            $("#"+form_name+"_edit_form #"+key).val(values[key]);
        }
        else
        {
            $("#"+form_name+"_view_form #"+key).text(values[key]); 
            $("#"+form_name+"_edit_form #"+key).val(values[key]);
        }
    }  
};
function save(form_name, event, params){
    var inputs = $("#"+form_name+"_edit_form").serializeArray();
    
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
    }
    function success() {
        bind_values(params, form_name);
    }
    function error() {
    }
    if(form_name == 'social'){
        ['twitter', 'facebook', 'linkedin'].forEach(function(attr, ind){
            params[attr] = [params[attr+"-label"], params[attr+"-url"]]
            delete params[attr+"-label"];
            delete params[attr+"-url"];
        });
    } 
    jsonrpc(event, params, success, error);
    $("#"+form_name+"_edit_form").hide();
    $("#"+form_name+"_view_form").show();
    return params
};
    
function edit(form_name){
    $("#"+form_name+"_view_form").hide();
    $("#"+form_name+"_edit_form").show();
};
