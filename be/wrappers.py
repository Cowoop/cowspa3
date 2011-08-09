import be.repository.pgdb as pgdb

pg_provider = pgdb.PGProvider()

def pg_transaction(f):
    def wrapper(*args, **kw):
        pg_provider.tr_start(env.context)
        try:
            res = f(*args, **kw)
        except:
            pg_provider.tr_abort(env.context)
            raise
        finally:
            pg_provider.tr_complete(env.context)
        return res
    return wrapper
pg_transaction.prop = 'pgdb'
pg_transaction.default = True


