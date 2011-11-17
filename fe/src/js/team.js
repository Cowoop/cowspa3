$('#team_form').hide();

$('#new-team').click(function() {
    $('#team_form').show();
});

$('#save-btn').click(function() {
    $('#team_form').hide();
    return false; //Temporarily - Remove once jsonrpc call is added
});
