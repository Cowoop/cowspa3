$(document).ready(function() {
    function success(response) {
        response['result'].forEach(function(activity){
            $('#activities').append("<li>"+activity+"</li>");
        });
        };
    function error() {
        };   
    jsonrpc('current.activities', {}, success, error);
    });
