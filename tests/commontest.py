try:
    import builtins
except:
    import __builtin__ as builtins

import sys
sys.path.append('.')

import psycopg2
import psycopg2.extras
import psycopg2.pool
import conf_local
import be.bootstrap
import be.apis.user

def load_apis():
    import be.apps

def setup_test_env():
    be.bootstrap.start()
    if not env.config.mode == 'TEST':
        sys.stderr.write('Not in TEST mode\n')
        sys.exit(1)
    load_apis()

def setup_system_context():
    be.apis.user.set_context(env.config.system_username, 0)

def destroy_test_env():
    import be.repository.stores as storeslib
    print( storeslib.known_stores.values())
    for store in storeslib.known_stores.values():
        store.destroy()

def jsonrpc(app, authtoken, context, api, params):
    return app.dispatch(authtoken, context, {"jsonrpc": "2.0", "method": api, "params": params, "id": 1})
