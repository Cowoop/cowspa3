var viewControl  = {
                resource_name : ko.observable(),
                short_desc : ko.observable(),
                long_desc : ko.observable(), 
                type : ko.observable(Array($("SELECT#type_list").val())),
                quantity_unit : ko.observable(),
                time_based : ko.observable(false),
                clicked :   function () {
                            var params = {  'name' : this.resource_name(),
                                            'short_description' : this.short_desc(),
                                            'long_description': this.long_desc(), 
                                            'type' : this.type()[0],
                                            'time_based' : this.time_based(),
                                            'quantity_unit' : this.quantity_unit()
                                            };
                            function success() {
                                $('#CreateResource-msg').html("<big>☑</big> Resource Created successful.");
                                };
                            function error() {
                                $('#CreateResource-msg').html("<big>Error in Resource Creation. Try again</big>");
                                };
                            jsonrpc('resource.new', params, success, error);
                }};
ko.applyBindings(viewControl);
