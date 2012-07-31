function ActivitiesViewModel() {
    var self = this;
    self.activities = ko.observableArray([]);
};

var model = new ActivitiesViewModel();
ko.applyBindings(model);

function on_activities(response) {
    var activities = response.result;
    for (var i=0; i < activities.length; i++) {
        model.activities.push(activities[i]);
    };
};

function error() { };

jsonrpc('activities.recent', {}, on_activities, error);

function on_roles(roles) {
    if (roles.length == 0) {
        $('.sidebar').show();
    };
}
