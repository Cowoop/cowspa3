import abc
import itertools
import psycopg2
import cPickle

from commonlib.helpers import odict

class BaseStore(object):
    def setup(self):
        raise NotImplemented

    def add(self, **data):
        raise NotImplemented
    def get(self, oid, fields, hashrows=True):
        """
        fields: list of field names
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
    def get_many(self, oids, fields=None, hashrows=True, order_by=None):
        """
        returns list of dicts keyed by field names
        """
        raise NotImplemented
    def get_all(self, fields=None, hashrows=True, order_by=None):
        """
        returns list of dicts keyed by field names
        """
    def get_by(self, crit, fields=None, hashrows=True, order_by=None):
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
    def remove_many(self, oids):
        raise NotImplemented
    def remove_by(self, crit):
        raise NotImplemented
    def update(self, oid, **mod_data):
        raise NotImplemented
    def update_many(self, oids, **mod_data):
        raise NotImplemented
    def update_by(self, crit, **mod_data):
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


class PGBinary(object):
    @classmethod
    def to_pg(self, data):
        if data == None:
            return None
        return psycopg2.Binary(cPickle.dumps(data, -1))
    @classmethod
    def to_python(self, data_s):
        if data_s == None:
            return None
        return cPickle.loads(str(data_s))


class PGStore(BaseStore):

    odicter = odict
    table_name = None
    cursor_getter = None # override
    schema = {}
    auto_id = False
    parent_stores = None
    pickle_cols = []

    def setup(self):
        if self.parent_stores:
            for store in self.parent_stores:
                store.setup()
        if not self.table_name:
            self.table_name = self.__class__.__name__.lower()
        self.load_schema()

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
            try:
                print(cursor.mogrify(q, values))
            except:
                print("damn, can't even mogrify: [%s], [%s]" % (q, values))
            raise
        if cursor.description:
            cols = tuple(r[0] for r in cursor.description)
            pickle_col_pos = [num for num, col in enumerate(cols) if col in self.pickle_cols]
            rows = [list(row) for row in cursor.fetchall()]
            for row in rows:
                for pos in pickle_col_pos:
                    row[pos] = PGBinary.to_python(row[pos])
            if hashrows:
                return [self.odicter(zip(cols, v)) for v in rows]
            return rows

    def add(self, **data):
        cols = list(data.keys())
        cols_to_pickle = set(cols).intersection(self.pickle_cols)
        cols_str = ', '.join(cols)
        values_str = ', '.join( ['%s' for i in cols] )
        q = 'INSERT INTO %(table_name)s (%(cols)s) VALUES (%(values_str)s)' % \
            dict(table_name=self.table_name, cols=cols_str, values_str=values_str)
        for col in cols_to_pickle:
            data[col] = PGBinary.to_pg(data[col])
        values = tuple(data[k] for k in cols)
        self.query_exec(q, values)
        if self.auto_id:
            cursor = self.cursor_getter()
            q = 'SELECT lastval()'
            cursor.execute(q)
            oid = cursor.fetchone()[0]
            return oid
        return True

    def add_many(self, items):
        """
        items: list of dicts
        returns ONLY oid of last item added. TODO: can we get oids of all the items without using executemany
        """
        cols = list(items[0].keys())
        cols_str = ', '.join(cols)
        value_str = '(' + (', '.join( [('%s') for c in cols] )) + ')'
        values_str = ', '.join((value_str for i in items))
        q = 'INSERT INTO %(table_name)s (%(cols)s) VALUES %(values_str)s' % \
            dict(table_name=self.table_name, cols=cols_str, values_str=values_str)
        cols_to_pickle = set(cols).intersection(self.pickle_cols)
        for item in items:
            for col in cols_to_pickle:
                item[col] = PGBinary.to_pg(item[col])
        values = tuple(itertools.chain(*(tuple(item[c] for c in cols) for item in items)))
        self.query_exec(q, tuple(values))
        if self.auto_id:
            cursor = self.cursor_getter()
            q = 'SELECT lastval()'
            cursor.execute(q)
            oid = cursor.fetchone()[0]
            return oid
        return True

    def get(self, oid, fields=[], hashrows=True):
        """
        oid: object id. match with id field of row.
        fields: fields to include in result. None return all.
            if only one field is specfied hashrows is ignored and single value (not a row) is returned
        hashrows: if True row(s) returned in form of a dictionary with column names as keys, else row tuple are returned
        returns jsonable odict keyed by field names
        """
        if isinstance(fields, basestring):
            fields = [fields]
        fields_len = len(fields)
        cols_str = self.fields2cols(fields)
        q = "SELECT %(cols_str)s FROM %(table_name)s WHERE id = %%s" %dict(table_name=self.table_name, cols_str=cols_str)
        hashrows = hashrows and not (fields_len == 1)
        ret = self.query_exec(q, (oid,), hashrows=hashrows)[0]
        if fields_len == 1:
            ret = ret[0]
        return ret

    def get_by(self, crit, fields=[], hashrows=True, limit=None, order_by=None):
        """
        crit: eg. name='Joe', lang='en'
        -> odict
        """
        cols_str = self.fields2cols(fields)
        # None (NULL) does not support = operator so needs special handling
        crit_keys_s = ' AND '.join(('%s = %%(%s)s' if v is not None else '%s is %%(%s)s') % (k,k) for k,v in crit.items())
        table_name = self.table_name
        q = 'SELECT %(cols_str)s FROM %(table_name)s WHERE %(crit_keys_s)s' % locals()
        if order_by: q = q + ' ORDER BY ' + order_by
        if limit: q = q + ' LIMIT %d' % limit
        return self.query_exec(q, crit, hashrows=hashrows)

    def get_one_by(self, crit, fields=[], hashrows=True):
        """
        @crit: criteria dict. all records matching with crit field key-values are returned
        returns list of dicts keyed by field names
        """
        return self.get_by(crit, fields, hashrows)[0]

    def get_one_by_safe(self, crit, fields=[], hashrows=True):
        """
        """
        try:
            return self.get_one_by(crit, fields, hashrows)
        except Exception as err:
            pass

    def get_many(self, oids, fields=[], hashrows=True, order_by=None):
        """
        returns list of dicts keyed by field names
        """
        if oids:
            cursor = self.cursor_getter()
            clause = "id IN %s"
            if order_by: clause += ' ORDER BY ' + order_by
            clause_values = (tuple(oids),)
            return self.get_by_clause(clause, clause_values, fields, hashrows)
        return []

    def get_all(self, fields=[], hashrows=True, order_by=None):
        """
        returns list of dicts keyed by field names
        """
        cols_str = self.fields2cols(fields)
        q = "SELECT %(cols_str)s FROM %(table_name)s" %dict(table_name=self.table_name, cols_str=cols_str)
        if order_by: q += ' ORDER BY ' + order_by
        return self.query_exec(q, hashrows=hashrows)

    def get_by_clause(self, clause, clause_values, fields=[], hashrows=True):
        cols_str = self.fields2cols(fields)
        q = "SELECT %(cols_str)s FROM %(table_name)s WHERE %(clause)s" % \
            dict(table_name=self.table_name, cols_str=cols_str, clause=clause)
        return self.query_exec(q, clause_values, hashrows=hashrows)

    def get_one_by_clause(self, clause, clause_values, fields=[], hashrows=True):
        return self.get_by_clause(clause, clause_values, fields, hashrows)[0]

    def update(self, oid, **mod_data):
        """
        update rows based on mod_data passed
        mod_data: dict
        -> True/False
        """
        cols = mod_data.keys()
        cols_to_pickle = set(cols).intersection(self.pickle_cols)
        cols_str = ', '.join('%s=%%(%s)s' % (k,k) for k in mod_data.keys())
        table_name = self.table_name
        q = 'UPDATE %(table_name)s SET %(cols)s WHERE id = %%(oid)s' % dict(table_name=table_name, cols=cols_str)
        values = dict((k, mod_data[k]) for k in cols)
        for col in cols_to_pickle:
            values[col] = PGBinary.to_pg(values[col])
        values['oid'] = oid
        self.query_exec(q, values)
        return True
        
    def update_many(self, oids, **mod_data):
        
        """update rows based on mod_data passed
        mod_data: dict
        -> True/False
        """
        cols = mod_data.keys()
        cols_to_pickle = set(cols).intersection(self.pickle_cols)
        cols_str = ', '.join('%s=%%(%s)s' % (k,k) for k in mod_data.keys())
        table_name = self.table_name
        q = 'UPDATE %(table_name)s SET %(cols)s WHERE id IN %%(oids)s' % dict(table_name=table_name, cols=cols_str)
        values = dict((k, mod_data[k]) for k in cols)
        for col in cols_to_pickle:
            values[col] = PGBinary.to_pg(values[col])
        values['oids'] = tuple(oids)
        self.query_exec(q, values)
        return True

    def update_by(self, crit, **mod_data):
        """
        """
        crit_keys = crit.keys()
        values = [crit[k] for k in crit_keys]
        condition = ' AND '.join(('%s = %%s' % k for k in crit_keys))
        cols = mod_data.keys()
        cols_to_pickle = set(cols).intersection(self.pickle_cols)
        cols_str = ', '.join('%s=%%s' % k for k in mod_data.keys())
        table_name = self.table_name
        q = 'UPDATE %(name)s SET %(cols)s WHERE %(condition)s' % dict(name=table_name, cols=cols_str, condition=condition)
        for col in cols_to_pickle:
            mod_data[col] = PGBinary.to_pg(mod_data[col])
        values = [mod_data[k] for k in cols] + values
        self.query_exec(q, values)
        return True

    def remove(self, oid):
        q = "DELETE FROM %s WHERE id = %%s" % self.table_name
        self.query_exec(q, (oid,))
        return True
    
    def remove_many(self, oids):
        q = "DELETE FROM %s WHERE id IN %%s" % self.table_name
        self.query_exec(q, (tuple(oids),))
        return True

    def remove_by(self, crit):
        crit_keys = crit.keys()
        values = [crit[k] for k in crit_keys]
        crit_keys_s = ', '.join(('%s = %%s' % k for k in crit_keys))
        table_name = self.table_name
        q = 'DELETE FROM %(table_name)s WHERE %(crit_keys_s)s' % locals()
        self.query_exec(q, values)
        return True

    def remove_by_clause(self, clause, clause_values):
        table_name = self.table_name
        q = 'DELETE FROM %(table_name)s WHERE %(clause)s' % locals()
        self.query_exec(q, clause_values)
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
        else:
            print("Does not exist:", self.table_name)

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
