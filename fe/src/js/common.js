$.jsonRPC.setup({
    endPoint: '/app',
    namespace: ''
});

function jsonrpc(apiname, params, success, error) {
    $.jsonRPC.request(apiname, {
        params: params,
        success: success,
        error: error
    });
};    
