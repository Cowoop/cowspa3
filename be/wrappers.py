import sys
import traceback
import be.repository.pgdb as pgdb
import be.errors
import be.libs.accesscontrol

pg_provider = pgdb.PGProvider()

def pg_transaction(f, pref):
    def wrapper(*args, **kw):
        try:
            res = f(*args, **kw)
        except:
            traceback.print_exc(file=sys.stdout)
            pg_provider.tr_abort(env.context)
            raise
        return res
    return wrapper
pg_transaction.prop = 'pgdb'

def access_check(f, pref):
    access_check = pref or be.libs.accesscontrol.Authenticated()
    def wrapper(*args, **kw):
        if access_check():
            res = f(*args, **kw)
        else:
            msg = 'API [%s] failed access check [%s]' % (f.__name__, access_check.__class__.__name__)
            raise be.errors.SecurityViolation(msg, {})
        return res
    return wrapper
access_check.prop = 'access'
