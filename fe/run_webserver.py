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

import commonlib.helpers as helpers

static_root = 'pub'
landing_pages = dict(member='booking/new', host='dashboard', director='dashboard', new='/new', admin='dashboard')

def construct_home_url(auth_token, context):
    home_url = 'login'
    if auth_token:
        json = dict(method='login', id=1, jsonrpc="2.0", params=dict(username=None, password=None, auth_token=auth_token))
        data = cowspa.dispatch(auth_token, json)
        if 'result' in data:
            roles = data['result']['roles']
            pref = data['result']['pref']
            no_roles = len(roles)
            if no_roles == 0:
                rolename = 'new'
            else:
                for role in roles:
                    if role['context'] == context:
                        rolename = role['roles'][0]['role']
                        break
                else:
                    rolename = roles[0]['roles'][0]['role']
                    context = roles[0]['context']

            landing_page = landing_pages[rolename]
            if landing_page.startswith('/'):
                home_url = landing_page
            else:
                home_url = '%(lang)s/%(rolename)s/%(theme)s/%(page)s' % \
                    dict(rolename=rolename, theme=pref.theme, lang='en', page=landing_pages[rolename])

    return home_url, context

@app.route('/new')
def new():
    return "You have no membership yet.", 200, {'Content-Type': 'text/html' +'; charset=utf-8'}

@app.route('/')
def index():
    auth_token = request.cookies.get('authcookie')
    context = int(request.cookies.get('current_ctx', 0))
    next_url, context = construct_home_url(auth_token, context)
    response = redirect(next_url)
    if context is not None:
        response.set_cookie('current_ctx',value=context)
    try:
        response.set_cookie('user_id', value=env.context.user_id)
        response.set_cookie('roles', value=env.context.roles)
    except:
        pass
    return response

@app.route('/search/<entity>', methods=['GET', 'POST'])
def search(entity):
    auth_token = request.cookies.get('authcookie')
    params = dict(
        q = request.args.get('q') or request.args.get('term'),
        context = request.args.get('context'),
        options = request.args.get('options', {}) )
    params = {"jsonrpc": "2.0", "method": "members.search", "params": params, "id": 1}
    data = cowspa.dispatch(auth_token, params)
    return helpers.jsonify(data['result'])

@app.route('/swf/<file_name>', methods=['GET', 'POST'])
def get_swf(file_name):
    path = "fe/contrib/swf/%s.swf" % (file_name)
    content_type = "application/swf"
    return file(path).read(), 200, {'Content-Type': content_type +'; charset=utf-8', 'Content-Disposition': 'filename=copy_cvs_xls_pdf.swf'}

@app.route('/invoice/<oid>/<format>', methods=['GET', 'POST'])
def get_invoice(oid, format):
    path = "%s/%s.%s" % (invoicelib.invoice_storage_dir, oid, format)
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
    parser = argparse.ArgumentParser(description='Run cowspa server.')
    parser.add_argument('-d', '--dev', action="store_true", default=False, help='Development mode. Caching turned off')
    parser.add_argument('-c', '--conf', action="store", default="prod", help='Conf mode. Load conf from conf_<mode>.py')
    args = parser.parse_args()
    if args.dev :
        print('Development mode ON. Caching turned OFF')
    else:
        print('Production mode ON. Caching turned ON')

    import be.bootstrap
    import be.apis.user as userlib
    be.bootstrap.start('conf_' + args.conf, args.dev)
    import be.apps
    cowspa = be.apps.cowspa
    import be.apis.invoice as invoicelib


    app = SharedDataMiddleware(app, {
            '/': static_root,
        }, fallback_mimetype="text/html", cache=not args.dev, cache_timeout=31536000)

    if env.config.threaded:
        app.run('0.0.0.0', debug=args.dev)

    from gevent.wsgi import WSGIServer

    hostname = env.config.hostname
    port = env.config.port

    http_server = WSGIServer((hostname, int(port)), app) # typecast to int in case a string is entered e.g. port = '5000'
    http_server.serve_forever()
