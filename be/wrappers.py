import sys
import traceback
import be.repository.pgdb as pgdb

pg_provider = pgdb.PGProvider()

def pg_transaction(f):
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
pg_transaction.default = True


