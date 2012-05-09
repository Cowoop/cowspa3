import commonlib
import commonlib.readconf as readconf
import commonlib.helpers
import commonlib.messaging.email
import bases.persistence as persistence
import be.repository.pgdb as pgdb
import be.repository.access as dbaccess
import conf_default

def setup_process_model(use_gevent=True):
    if use_gevent:
        import gevent
        import gevent.monkey
        import gevent.local as localprov
        gevent.monkey.patch_all()
        import psyco_gevent
        psyco_gevent.make_psycopg_green()
    else:
        import threading
        localprov = threading
    return localprov

def setup_env():
    class env: pass
    env.config = readconf.parse_config()
    use_gevent = not env.config.threaded
    localprov = setup_process_model(use_gevent)
    commonlib.helpers.random_key_gen = commonlib.helpers.RandomKeyFactory(env.config.random_str)
    env.mailer = commonlib.messaging.email.Mailer(env.config.mail)
    env.mailer.start()
    env.context = localprov.local()
    commonlib.helpers.push_to_builtins('env', env)
    return env

def setup_stores():
    dependent_stores = []
    for name in dir(dbaccess.stores):
        store = getattr(dbaccess.stores, name)
        if hasattr(store, 'setup'):
            store.setup()

def setup_pg_provider():
    provider = pgdb.PGProvider(env.config.threaded)
    provider.startup()
    return provider

def start():
    commonlib.helpers.setdefaultencoding()
    env = setup_env()
    env.__cs_debug__ = env.config.mode in ('DEV', 'TEST')
    provider = setup_pg_provider()
    provider.tr_start(env.context)
    setup_stores()
    provider.tr_complete(env.context)
    provider.tr_start(env.context) # This is to make sure other db transactions in same thread works. Such as Test cases.

#start()
