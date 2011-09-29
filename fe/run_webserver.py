import os
import sys
from jsonrpc2 import JsonRpc
import simplejson

path = os.path.abspath(os.getcwd())
sys.path.insert(0, '.')
sys.path.insert(0, '..')

from flask import Flask, jsonify, url_for, session, redirect, request
app = Flask(__name__)
app.secret_key = os.urandom(24)

static_root = 'pub'
import be.apis.user as userlib
import be.bootstrap
be.bootstrap.start('conf_test')
import be.apps
cowspa = be.apps.cowspa

@app.route('/search/<entity>', methods=['GET', 'POST'])
def search(entity):
    auth_token = request.cookies.get('authcookie')
    cowspa.tr_start()
    if auth_token:
        userlib.set_context_by_session(auth_token)
    q = request.args.get('q') or request.args.get('term')
    params = {"jsonrpc": "2.0", "method": entity+".search", "params": {'q':q}, "id": 1}
    data = cowspa.mapper(params)
    cowspa.tr_complete()
    if 'result' in data:
        return simplejson.dumps(data['result'])
    else:
        return jsonify(data)

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
            cowspa.tr_start()
    #params = rpc({"jsonrpc": "2.0", "method": methodname, "params": params, "id": 1})
    data = cowspa.mapper(params)
    if params['method'] == 'login' and 'result' in data:
        auth_token = data['result']
        data['result'] = userlib.get_user_preferences()
        cowspa.tr_complete()
        resp = jsonify(data)
        resp.set_cookie('authcookie',value=auth_token)
        resp.set_cookie('user_id',value=env.context.user_id)
        resp.set_cookie('roles',value=env.context.roles)
        return resp
    cowspa.tr_complete()
    return jsonify(data)

@app.route('/', methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def static(path='login'):
    print '====>', path
    fspath = os.path.join(static_root, path)
    filename = os.path.basename(path)
    if '.' in path:
        content_type = "text/" + path.split('.')[-1]
    else:
        content_type = "text/html"
    return file(fspath).read(), 200, {'Content-Type': content_type +'; charset=utf-8', "Cache-Control": "max-age=31536000"}

if __name__ == '__main__':
    if env.config.threaded:
        app.run('0.0.0.0',debug=False)

    from gevent.wsgi import WSGIServer

    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
