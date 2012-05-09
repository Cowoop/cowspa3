import psycopg2
import psycopg2.pool
import bases.persistence as persistence

pool = None

class PGProvider(persistence.DBProvider):
    def __init__(self, threaded=False):
        self.threaded = threaded

    def tr_start(self, context):
        conn = pool.getconn()
        # print '======= DB connections [', len(pool._used), ']=================='
        context.pgcursor = conn.cursor()

    def tr_complete(self, context):
        cur = context.pgcursor
        cur.connection.commit()
        cur.close()
        pool.putconn(cur.connection)
        # print '======= tr_complete DB connections [', len(pool._used), ']=================='

    def tr_abort(self, context):
        cur = context.pgcursor
        cur.execute('abort')
        # print '======= tr_abort DB connections [', len(pool._used), ']=================='

    def startup(self):
        global pool
        if self.threaded:
            pool = psycopg2.pool.PersistentConnectionPool(5, 10, **env.config.pgdb)
        else:
            pool = psycopg2.pool.SimpleConnectionPool(5, 10, **env.config.pgdb)

    def shutdown(self):
        pool.close_all()
