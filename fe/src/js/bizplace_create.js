var viewControl  = {
                biz_id : ko.observable(Array($("SELECT#biz_id").val())),
                name : ko.observable(),
                address : ko.observable(),
                city : ko.observable(), 
                country : ko.observable(Array($("SELECT#country").val())),
                short_desc : ko.observable(),
                email : ko.observable(),
                clicked :   function () {
                            var params = {  'biz_id' : parseInt(this.biz_id()[0]),
                                            'name' : this.name(),
                                            'address' : this.address(),
                                            'city': this.city(), 
                                            'country': this.country()[0], 
                                            'email' : this.email(),
                                            'short_description' : this.short_desc()
                                            };
                            function success() {
                                $('#CreateBizplace-msg').html("<big>☑</big> Bizplace Created successful.");
                                };
                            function error() {
                                $('#CreateBizplace-msg').html("<big>Error in Bizplace Creation. Try again</big>");
                                };
                            jsonrpc('bizplace.new', params, success, error);
                }};
ko.applyBindings(viewControl);
