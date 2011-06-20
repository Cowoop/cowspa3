try:
    import builtins
except:
    import __builtin__ as builtins

import sys
import psycopg2
import psycopg2.extras
import psycopg2.pool
import conf_test
import be.bootstrap

sys.path.append('.')

def setup_test_cursor():
    pool = psycopg2.pool.SimpleConnectionPool(5, 5, conf_test.config['pg_uri'])
    cursor = pool.getconn().cursor()
    cursor_getter = lambda x=None: cursor
    return cursor_getter

def setup_test_simple_env():
    cursor_getter = setup_test_cursor()
    class env:
        class context:
            pgcursor = cursor_getter()
    builtins.env = env

def setup_test_env():
    be.bootstrap.start('conf_test')

def destroy_test_env():
    import be.repository.stores as storeslib
    print( storeslib.known_stores.values())
    for store in storeslib.known_stores.values():
        store.destroy()
