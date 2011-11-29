import os
import sys
from jsonrpc2 import JsonRpc

path = os.path.abspath(os.getcwd())
sys.path.insert(0, '.')
sys.path.insert(0, '..')

from flask import Flask, url_for, session, redirect, request
from werkzeug.wsgi import SharedDataMiddleware
app = Flask(__name__)
app.secret_key = os.urandom(24)

static_root = 'pub'
import be.apis.user as userlib
import be.apis.member as memberlib
import be.bootstrap
be.bootstrap.start('conf_test')
import be.apps
cowspa = be.apps.cowspa
import commonlib.helpers as helpers
        
@app.route('/search/<entity>', methods=['GET', 'POST'])
def search(entity):
    auth_token = request.cookies.get('authcookie')
    cowspa.tr_start()
    if auth_token:
        userlib.set_context_by_session(auth_token)
    q = request.args.get('q') or request.args.get('term')
    params = {"jsonrpc": "2.0", "method": "members.search", "params": {'q':q, 'mtype':entity}, "id": 1}
    print entity
    data = cowspa.mapper(params)
    cowspa.tr_complete()
    if 'result' in data:
        return helpers.jsonify(data['result'])
    else:
        return helpers.jsonify(data)

@app.route('/invoice/<oid>/<format>', methods=['GET', 'POST'])
def get_invoices(oid, format):
    path = "be/repository/invoices/invoice_%s.%s" % (oid, format)
    if format == "pdf":
        content_type = "application/pdf"
    else:
        content_type = "text/html"
    return file(path).read(), 200, {'Content-Type': content_type +'; charset=utf-8', 'Content-Disposition': 'filename=invoice_'+oid}

@app.route('/app', methods=['GET', 'POST'])
def api_dispatch():
    params = request.json
    auth_token = request.cookies.get('authcookie')
    cowspa.tr_start()
    if auth_token:
        try:
            userlib.set_context_by_session(auth_token)
        except:
            cowspa.tr_abort()
    try:
        data = cowspa.mapper(params)
        #params = rpc({"jsonrpc": "2.0", "method": methodname, "params": params, "id": 1})
        if params['method'] == 'login' and 'result' in data:
            auth_token = data['result']
            data['result'] = userlib.get_user_preferences()
            resp = helpers.jsonify(data)
            resp.set_cookie('authcookie',value=auth_token)
            resp.set_cookie('user_id',value=env.context.user_id)
            resp.set_cookie('roles',value=env.context.roles)
            resp.set_cookie('member_name', value=memberlib.member_resource.get(env.context.user_id, 'name'))
            cowspa.tr_complete()
            return resp
    except:
        cowspa.tr_abort()
    cowspa.tr_complete()
    return helpers.jsonify(data)

app = SharedDataMiddleware(app, {
        '/': static_root,
}, fallback_mimetype="text/html", cache=True, cache_timeout=31536000)

if __name__ == '__main__':
    if env.config.threaded:
        app.run('0.0.0.0',debug=False)

    from gevent.wsgi import WSGIServer

    http_server = WSGIServer(('', 5001), app)
    http_server.serve_forever()
