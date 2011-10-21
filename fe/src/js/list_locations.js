$(document).ready(function() {
    var params = {};

    function success(resp) {
        $('#loc_tmpl').tmpl(resp['result']).appendTo('#location-list');
    };

    function error() {
    };

    params = {'owner':$.cookie('user_id')};
    jsonrpc('bizplace.list', params, success, error);
});