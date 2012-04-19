//*****************************Global Section***********************************
var picture = null;
var image_size_limit = 256000;//256kb
var calc_modes = {quantity_based: 0, time_based: 1, monthly: 2}

function ResourceViewModel(invoice) {
    var self = this;
    self.resource_type = ko.observable('room');
    self.time_based = ko.observable(true);
    self.calendar = ko.observable(true);

    self.resource_type.subscribe(function(type) {
        var is_room = (type == 'room');
        self.time_based(is_room);
        self.calendar(is_room);
    });
};

model = new ResourceViewModel();
ko.applyBindings(model);
//xxxxxxxxxxxxxxxxxxxxxxxxxxxEnd Global Sectionxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

//****************************Save Resource*************************************

function create_resource (form) {
    var theform = $(form);
    theform.checkValidity();
    var action_status = $('.action-status');
    action_status.text("Creating resource ...");
    var inputs = theform.serializeArray();
    var params = {}
    for(var i in inputs){
        params[inputs[i].name] = inputs[i].value;
    }
    params.owner = current_ctx;    
    params.picture = picture;
    params.calc_mode = model.time_based() ? calc_modes.time_based : calc_modes.quantity_based;
    params.calendar = model.calendar();
    function success() {
        action_status.text("Resource created successfully").attr('class', 'status-success');
        setTimeout(function(){
            window.location = basepath + '/resources';
        }, 1000);
    };
    function error() {
        action_status.text("Error in creating resource").attr('class', 'status-fail');
    };
    jsonrpc('resource.new', params, success, error);
};

//xxxxxxxxxxxxxxxxxxxxxxxxxxxEnd Save Resourcexxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

//***************************Upload Resource Picture****************************
$('#picture').change(function handleFileSelect(evt) {
    var files = evt.target.files;
    var reader = new FileReader();
    reader.onload = (function(e) {
        picture = e.target.result;
    });
    if(files.length == 1){
        if(files[0].size <= image_size_limit)
            reader.readAsDataURL(files[0]);
        else
            alert("Image size exceeds image upload limit, Image size must be less than "+ (image_size_limit/1000) + "kb.");
    }
});
//xxxxxxxxxxxxxxxxxxxxxxxxxEnd Upload Invoice Picturexxxxxxxxxxxxxxxxxxxxxxxxxxx
