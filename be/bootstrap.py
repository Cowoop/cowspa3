try:
    import builtins
except:
    import __builtin__ as builtins # Python 2.x compatibility

import commonlib
import commonlib.readconf as readconf
import commonlib.helpers
import commonlib.messaging.email
import bases.persistence as persistence
import be.repository.pgdb as pgdb
import be.repository.access as dbaccess
import conf_default
try:
    import gevent
    import gevent.local as localprov
except:
    import threading
    localprov = threading

def setdefaultencoding():
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

def setup_env(conf):
    class env: pass
    try:
        conf_local = __import__(conf)
    except Exception as err:
        print(err)
        conf_local = None
    env.config = readconf.parse_config(conf_default, conf_local)
    commonlib.helpers.random_key_gen = commonlib.helpers.RandomKeyFactory(env.config.random_str)
    #env.mailer = commonlib.messaging.email.Mailer(env.config.mail)
    #env.mailer.start()
    env.context = localprov.local()
    builtins.env = env
    return env

def setup_stores():
    dependent_stores = []
    for name in dir(dbaccess.stores):
        store = getattr(dbaccess.stores, name)
        if hasattr(store, 'setup'):
            store.setup()

def setup_pg_provider():
    provider = pgdb.PGProvider()
    provider.startup()
    return provider

def start(conf):
    env = setup_env(conf)
    env.__cs_debug__ = conf != 'conf_prod'
    provider = setup_pg_provider()
    provider.tr_start()
    setup_stores()
    provider.tr_complete()
    env.pg_provider = provider

#start(conf='conf_dev')
