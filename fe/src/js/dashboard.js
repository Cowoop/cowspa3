function success(response) {
    response.result.forEach(function(activity){
        $('ul#activities').append("<li class='activity'></li>");
        $('ul#activities li:last-child').html(activity.message);
    });
};
function error() { };   
jsonrpc('activities.recent', {}, success, error);


function on_roles(roles) {
    if (roles.length == 0) {
        $('.sidebar').show();
    };
}
