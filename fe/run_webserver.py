import os
import sys
from jsonrpc2 import JsonRpc

path = os.path.abspath(os.getcwd())
sys.path.insert(0, '.')
sys.path.insert(0, '..')

from flask import Flask, request, redirect
from werkzeug.wsgi import SharedDataMiddleware
app = Flask(__name__)
app.secret_key = os.urandom(24)

static_root = 'pub'
import be.bootstrap
import be.apis.user as userlib
be.bootstrap.start('conf_test')
import be.apps
cowspa = be.apps.cowspa
import commonlib.helpers as helpers
import be.apis.invoice as invoicelib

@app.route('/')
def index():
    return redirect('login')

@app.route('/search/<entity>', methods=['GET', 'POST'])
def search(entity):
    auth_token = request.cookies.get('authcookie')
    q = request.args.get('q') or request.args.get('term')
    params = {"jsonrpc": "2.0", "method": "members.search", "params": {'q':q, 'mtype':entity}, "id": 1}
    data = cowspa.dispatch(auth_token, params)
    return helpers.jsonify(data['result'])

@app.route('/invoice/<oid>/<format>', methods=['GET', 'POST'])
def get_invoice(oid, format):
    path = "%s/invoice_%s.%s" % (invoicelib.invoice_storage_dir, oid, format)
    if format == "pdf":
        content_type = "application/pdf"
    else:
        content_type = "text/html"
    return file(path).read(), 200, {'Content-Type': content_type +'; charset=utf-8', 'Content-Disposition': 'filename=invoice_'+oid}

@app.route('/app', methods=['GET', 'POST'])
def api_dispatch():
    auth_token = request.cookies.get('authcookie') if request.json.get('method') != 'login' else None
    # ex. request.json: {"jsonrpc": "2.0", "method": methodname, "params": params, "id": 1}
    data = cowspa.dispatch(auth_token, request.json)
    return helpers.jsonify(data)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Run cowspa webserver.')
    parser.add_argument('-d', '--dev', action="store_true", default=False, help='Development mode. Caching turned off')
    args = parser.parse_args()
    if args.dev :
        print('Development mode ON. Caching turned OFF')
    else:
        print('Production mode ON. Caching turned ON')

    app = SharedDataMiddleware(app, {
            '/': static_root,
        }, fallback_mimetype="text/html", cache=not args.dev, cache_timeout=31536000)

    if env.config.threaded:
        app.run('0.0.0.0',debug=False)

    from gevent.wsgi import WSGIServer

    http_server = WSGIServer(('', 5001), app)
    http_server.serve_forever()
