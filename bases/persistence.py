import abc
import psycopg2

from commonlib.helpers import odict

class BaseStore(object):
    def setup(self):
        raise NotImplemented

    def add(self, **data):
        raise NotImplemented
    def get(self, oid, fields, hashrows=True):
        """
        returns dict keyed by field names
        """
        raise NotImplemented
    def get_one_by(self, crit, fields=None, hashrows=True):
        """
        crit: eg. name='Joe', lang='en'
        -> odict
        """
    def get_one_by_safe(self, crit, fields=None, hashrows=True):
        """
        """
        try:
            return self.get_one_by(crit, fields, hashrows)
        except Exception as err:
            pass
    def get_many(self, oids, fields=None, hashrows=True):
        """
        returns list of dicts keyed by field names
        """
        raise NotImplemented
    def get_all(self, fields=None, hashrows=True):
        """
        returns list of dicts keyed by field names
        """
    def get_by(self, crit, fields=None, hashrows=True):
        """
        @crit: criteria dict. all records matching with crit field key-values are returned
        returns list of dicts keyed by field names
        """
        raise NotImplemented
    def get_by_clause(self, clause, clause_values, fields=None, hashrows=True):
        raise NotImplemented
    def update(self, oid, **mod_data):
        raise NotImplemented
    def remove(self, oid):
        raise NotImplemented
    def remove_by(self, crit):
        raise NotImplemented
    def query_exec(self, q, values, hashrows=True, log=False):
        """
        @q: object representing query to be executed
        @log: logs the query
        """
        raise NotImplemented
    def count(self):
        raise NotImplemented
    def destroy(self):
        """
        Destroys the store
        """
        raise NotImplemented


class PGStore(BaseStore):

    odicter = odict
    table_name = None
    cursor_getter = None # override
    schema = {}
    auto_id = False

    def setup(self):
        if self.parent_stores:
            for store in self.parent_stores:
                store.setup()
        if not self.table_name:
            self.table_name = self.__class__.__name__.lower()
        self.load_schema()

    def ref(self, oid):
        return self.__class__.__name__ + ':' + str(oid)

    def load_schema(self):
        cursor = self.cursor_getter()
        q = "select 1 from information_schema.tables where table_name = %s"
        cursor.execute(q, (self.table_name,))
        res = cursor.fetchone()
        if not res:
            self.create_table()
        q = "select column_name, column_default, character_maximum_length from INFORMATION_SCHEMA.COLUMNS where table_name=%s"
        cursor.execute(q, (self.table_name,))
        cols = cursor.fetchall()
        schema = {}
        for name, column_default, max_len in cols:
            schema[name] = odict(name=name, max_len=max_len)
            if name == 'id' and column_default == "nextval('%s_id_seq'::regclass)" % self.table_name:
                self.auto_id = True
        self.schema = schema

    def create_table(self, cursor=None):
        cursor = cursor or self.cursor_getter()
        print("Setting up: ", self.table_name)
        q = "CREATE TABLE %(table_name)s (%(sql)s)" % dict(table_name=self.table_name, sql=self.create_sql)
        if self.parent_stores:
            parent_tables_s = ', '.join((store.table_name for store in self.parent_stores))
            q = q + " INHERITS(%(parent_tables)s)" % dict(parent_tables=parent_tables_s) 
        try:
            self.query_exec(q)
        except psycopg2.ProgrammingError:
            raise

    def fields2cols(self, fields):
        cols_str = '*'
        if fields:
            cols_str = ', '.join(fields)
        return cols_str

    def query_exec(self, q, values=None, log=False, hashrows=True):
        """
        @q: object representing query to be executed
        @log: logs the query
        """
        cursor = self.cursor_getter()
        try:
            if getattr(env, '__cs_debug__', True):
                print(cursor.mogrify(q, values))
            cursor.execute(q, values)
        except psycopg2.ProgrammingError:
            print(cursor.mogrify(q, values))
            raise
        if cursor.description:
            cols = tuple(r[0] for r in cursor.description)
            values = cursor.fetchall()
            if hashrows:
                return [self.odicter(zip(cols, v)) for v in values]
            return values

    def add(self, **data):
        cols = list(data.keys())
        cols_str = ', '.join(cols)
        values_str = ', '.join( ['%s' for i in cols] )
        q = 'INSERT INTO %(table_name)s (%(cols)s) VALUES (%(values_str)s)' % \
            dict(table_name=self.table_name, cols=cols_str, values_str=values_str)
        values = tuple(data[k] for k in cols)
        self.query_exec(q, values)
        if self.auto_id:
            cursor = self.cursor_getter()
            q = 'SELECT lastval()'
            cursor.execute(q)
            oid = cursor.fetchone()[0]
            return oid
        return True

    def get(self, oid, fields=None, hashrows=True):
        """
        oid: object id. match with id field of row.
        fields: fields to include in result. None return all.
        returns jsonable odict keyed by field names
        """
        cols_str = self.fields2cols(fields)
        q = "SELECT %(cols_str)s FROM %(table_name)s WHERE id = %%s" %dict(table_name=self.table_name, cols_str=cols_str)
        return self.query_exec(q, (oid,), hashrows=hashrows)[0]

    def get_by(self, crit, fields=None, hashrows=True):
        """
        crit: eg. name='Joe', lang='en'
        -> odict
        """
        cols_str = self.fields2cols(fields)
        crit_keys = list(crit.keys())
        values = tuple(crit[k] for k in crit_keys)
        crit_keys_s = ' AND '.join(('%s = %%s' % k for k in crit_keys))
        table_name = self.table_name
        q = 'SELECT %(cols_str)s FROM %(table_name)s WHERE %(crit_keys_s)s' % locals()
        return self.query_exec(q, values, hashrows=hashrows)

    def get_one_by(self, crit, fields=None, hashrows=True):
        """
        @crit: criteria dict. all records matching with crit field key-values are returned
        returns list of dicts keyed by field names
        """
        return self.get_by(crit, fields, hashrows)[0]

    def get_one_by_safe(self, crit, fields=None, hashrows=True):
        """
        """
        try:
            return self.get_one_by(crit, fields, hashrows)
        except Exception as err:
            pass

    def get_many(self, oids, fields=None, hashrows=True):
        """
        returns list of dicts keyed by field names
        """
        cursor = self.cursor_getter()
        clause = "id IN %s"
        clause_values = (tuple(oids),)
        return self.get_by_clause(clause, clause_values, fields, hashrows)

    def get_all(self, fields=None, hashrows=True):
        """
        returns list of dicts keyed by field names
        """
        cols_str = self.fields2cols(fields)
        q = "SELECT %(cols_str)s FROM %(table_name)s" %dict(table_name=self.table_name, cols_str=cols_str)
        return self.query_exec(q, hashrows=hashrows)

    def get_by_clause(self, clause, clause_values, fields=None, hashrows=True):
        cols_str = self.fields2cols(fields)
        q = "SELECT %(cols_str)s FROM %(table_name)s WHERE %(clause)s" % \
            dict(table_name=self.table_name, cols_str=cols_str, clause=clause)
        return self.query_exec(q, clause_values, hashrows=hashrows)

    def get_one_by_clause(self, clause, clause_values, fields=None, hashrows=True):
        return self.get_by_clause(clause, clause_values, fields, hashrows)[0]

    def update(self, oid, **mod_data):
        """
        update a row based on mod_data passed
        mod_data: dict
        -> True/False
        """
        cols = mod_data.keys()
        cols_str = ', '.join('%s=%%(%s)s' % (k,k) for k in mod_data.keys())
        table_name = self.table_name
        q = 'UPDATE %(table_name)s SET %(cols)s WHERE id = %(oid)s' % dict(table_name=table_name, cols=cols_str, oid=oid)
        values = dict((k, mod_data[k]) for k in cols)
        self.query_exec(q, values)
        return True

    def update_by(self, crit, **mod_data):
        """
        """
        crit_keys = crit.keys()
        values = [crit[k] for k in crit_keys]
        condition = ', '.join(('%s = %%s' % k for k in crit_keys))
        cols = mod_data.keys()
        cols_str = ', '.join('%s=%%s' % k for k in mod_data.keys())
        table_name = self.table_name
        q = 'UPDATE %(name)s SET %(cols)s WHERE %(condition)s' % dict(name=table_name, cols=cols_str, condition=condition)
        values = [mod_data[k] for k in cols] + values
        self.query_exec(q, values)
        return True

    def remove(self, oid):
        q = "DELETE FROM %s WHERE id = %%s" % self.table_name
        self.query_exec(q, (oid,))
        return True

    def remove_by(self, crit):
        crit_keys = crit.keys()
        values = [crit[k] for k in crit_keys]
        crit_keys_s = ', '.join(('%s = %%s' % k for k in crit_keys))
        table_name = self.table_name
        q = 'DELETE FROM %(table_name)s WHERE %(crit_keys_s)s' % locals()
        self.query_exec(q, values)
        return True

    def count(self):
        """
        -> int
        """
        q = 'SELECT count(*) from %s' % self.table_name
        return self.query_exec(q, hashrows=False)[0][0]

    def destroy(self, cursor=None):
        cursor = cursor or self.cursor_getter()
        q = "select 1 from information_schema.tables where table_name = %s"
        cursor.execute(q, (self.table_name,))
        if cursor.fetchone():
            print("Destroying: ", self.table_name)
            q = 'DROP TABLE ' + self.table_name + ' CASCADE;'
            self.query_exec(q)

class DBProvider(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def startup(self):
        """
        """
    @abc.abstractmethod
    def shutdown(self):
        """
        """
    @abc.abstractmethod
    def tr_start(self, context):
        """
        context: context storage
        """
    @abc.abstractmethod
    def tr_abort(self, context):
        """
        """
    @abc.abstractmethod
    def tr_complete(self, context):
        """
        """

class PObject(object):
    def __init__(self, oid, ref_store):
        self.oid = oid
        self.ref_store = ref_store

    def ref(self):
        """
        returns object ref
        """
        return self.ref_store.ref(self.oid)

