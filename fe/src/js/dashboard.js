$(document).ready(function() {
    function success(response) {
        response['result'].forEach(function(activity){
            console.log(activity);
            $('ul#activities').append("<li class='activity'></li>");
            $('ul#activities li:last-child').html(activity.message);
        });
    };
    function error() { };   
    jsonrpc('current.activities', {}, success, error);
    });
