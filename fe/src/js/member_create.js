var viewControl  = {
                first_name : ko.observable(),
                last_name : ko.observable(),
                username : ko.observable(), 
                password : ko.observable(),
                re_password : ko.observable(),
                language : ko.observable(Array($("SELECT#language").val())),
                country : ko.observable(Array($("SELECT#location").val())),
                email : ko.observable(),
                clicked :   function () {
                            var params = {  'first_name' : this.first_name(),
                                            'last_name' : this.last_name(),
                                            'username' : this.username(), 
                                            'password' : this.password(),
                                            'language' : this.language()[0],
                                            'country' : this.country()[0], 
                                            'email' : this.email()
                                            };
                            function success() {
                                $('#CreateMember-msg').html("<big>☑</big> Member Created successful.");
                                };
                            function error() {
                                $('#CreateMember-msg').html("<big>Error in Member Creation. Try again</big>");
                                };
                            jsonrpc('member.new', params, success, error);
                }};
ko.applyBindings(viewControl);
