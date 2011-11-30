function success(response) {
    response.result.forEach(function(activity){
        $('ul#activities').append("<li class='activity'></li>");
        $('ul#activities li:last-child').html(activity.message);
    });
    if (response.result.length == 0) {
        $('.sidebar').show();
    };
};
function error() { };   
jsonrpc('activities.recent', {}, success, error);
