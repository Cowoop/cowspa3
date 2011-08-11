H5F.setup(document.getElementById('login_form'));
var viewControl  = {
                username : ko.observable(), 
                password : ko.observable(),
                clicked :   function () {
                            var params = {'username': this.username(), 'password': this.password()};
                            function success() {
                                $('#login-msg').html("<big>☑</big> Login is successful.");
                                };
                            function error() {
                                $('#login-msg').html("<big>Authentication Error. Try again</big>");
                                };
                            jsonrpc('login', params, success, error);
                }};
ko.applyBindings(viewControl);
