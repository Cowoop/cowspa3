H5F.setup(document.getElementById('createmember_form'));
$('#save-btn').click(function () {
    var params = {  
        'first_name' : $("input#first_name").val(),
        'last_name' : $("input#last_name").val(),
        'username' : $("input#username").val(),
        'password' : $("input#password").val(),
        'language' : $("select#language").val(),
        'country' : $("select#country").val(),
        'email' : $("input#email").val()
        }
    function success() {
        $('#CreateMember-msg').html("<big>☑</big> Member Created successful.");
        }
    function error() {
        $('#CreateMember-msg').html("<big>Error in Member Creation. Try again</big>");
        }
    jsonrpc('member.new', params, success, error);
    });
