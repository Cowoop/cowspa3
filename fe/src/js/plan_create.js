var viewControl  = {
                plan_name : ko.observable(),
                bizplace_id : ko.observable(Array($("SELECT#bizplace_ids").val())),
                description : ko.observable(), 
                clicked :   function () {
                            var params = {  'name' : this.plan_name(),
                                            'bizplace_id' : parseInt(this.bizplace_id()),
                                            'description': this.description()
                                            };
                            function success() {
                                $('#CreatePlan-msg').html("<big>☑</big> Plan Created successful.");
                                };
                            function error() {
                                $('#CreatePlan-msg').html("<big>Error in Plan Creation. Try again</big>");
                                };
                            jsonrpc('plan.new', params, success, error);
                }};
ko.applyBindings(viewControl);
