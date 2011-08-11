var viewControl  = {
                first_name : ko.observable(),
                username : ko.observable(), 
                password : ko.observable(),
                re_password : ko.observable(),
                bizplace_id : ko.observable(Array($("SELECT#bizplace_id").val())),
                email : ko.observable(),
                clicked :   function () {
                            var params = {  'first_name' : this.first_name(),
                                            'username' : this.username(), 
                                            'password' : this.password(),
                                            'context' : "Bizplace"+this.bizplace_id()[0], 
                                            'email' : this.email()
                                            };
                            function success() {
                                $('#CreateSuper-msg').html("<big>☑</big> Super User Created successfully.");
                                };
                            function error() {
                                $('#CreateSuper-msg').html("<big>Error in Super User Creation. Try again</big>");
                                };
                            jsonrpc('super', params, success, error);
                }};
ko.applyBindings(viewControl);
