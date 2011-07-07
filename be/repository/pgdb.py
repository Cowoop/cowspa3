import psycopg2
import psycopg2.pool
import bases.persistence as persistence

pool = None

class PGProvider(persistence.DBProvider):
    def tr_start(self):
        conn = pool.getconn()
        env.context.pgcursor = conn.cursor()

    def tr_complete(self):
        cur = env.context.pgcursor
        cur.connection.commit()
        pool.putconn(cur.connection)

    def tr_abort(self):
        cur = env.context.pgcursor
        cur.execute('abort')

    def startup(self):
        global pool
        pool = psycopg2.pool.SimpleConnectionPool(5, 5, env.config.pg_uri)

    def shutdown(self):
        pool.close_all()
