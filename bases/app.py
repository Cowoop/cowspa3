import werkzeug.exceptions
import werkzeug.routing as routing

import bases.errors as errors

class Application(object):
    def __init__(self):
        self.on_startup = []
        self.on_shutdown = []

    def startup(self):
        for f in self.on_startup:
            f()
            print self.name, ':startup::', f.__func__.__module__, '.', f.__name__
    def shutdown(self):
        # sys.atexit
        for f in self.on_shutdown:
            f()

class Collection(object):
    pass

class Resource(object):
    _get_methods = []
    _set_methods = []

class Mapper(object):
    def __init__(self, prefix=''):
        self.prefix = prefix if prefix and prefix[0] is '/' else '/' + prefix
        self.rules = []
        self._map = {}

    def append_rule(self, path, endpoint):
        self.rules.append(routing.Rule(self.prefix + path, endpoint=endpoint))

    def connect(self, path, func):
        self.append_rule(path, function)

    def connect_collection(self, path, collection):
        actions_available = ((name, getattr(collection, name)) for name in dir(collection) if \
            not name.startswith('_') and '__call__' in  dir(getattr(collection, name)))
        for name, f in actions_available:
            f_path = path + '/' + name
            self.append_rule(f_path, f)

    def connect_resource(self, path, resource):
        self.connect_collection(path, resource)

    def build(self):
        m = routing.Map(self.rules)
        return m.bind("cowspa.net", "/")

class Dispatcher(object):

    def __init__(self, locator, pg_provider, comps=[]):
        self.comps = comps
        self.locator = locator
        self.pg_provider = pg_provider

    def __getattr__(self, name):
        comps = object.__getattribute__(self, 'comps') + [name]
        locator = object.__getattribute__(self, 'locator')
        pg_provider = object.__getattribute__(self, 'pg_provider')
        dispatcher = Dispatcher(locator, pg_provider, comps)
        return dispatcher

    def set_context(self, user_id):
        env.context.user_id = user_id

    def run_checks(self, f, args, kw):

        perms_needed = getattr(f, 'perms', None)
        if perms_needed is not None:
            helpers.perm_checker(context, perms_needed)

        return f(*args, **kw)

    def __call__(self, *args, **kw):
        retcode = errors.success
        result = None

        # 1. Find the callable, return if not found
        path = '/' + ('/'.join(self.comps))
        try:
            f, _kw = self.locator.match(path)
        except AttributeError as err:
            retcode = errors.invalid_api
            return retcode, result

        # 2. Run all checks
        try:
            self.run_checks(f, args, kw)
        except errors.APIExecutionError as err:
            print('Error', err)
            return err.retcode, err.result
        except Exception as err:
            # log error
            print(err)
            return errors.uncaught_exception, result

        # 3. Start DB Transaction and execute the API
        try:
            self.pg_provider.tr_start()
            kw.update(_kw)
            result = f(*args, **kw)
            self.pg_provider.tr_complete()
        except errors.APIExecutionError as err:
            print(err)
            return err.retcode, err.result
        except Exception as err:
            print(err)
            # log error
            self.pg_provider.tr_abort()
            return errors.uncaught_exception, result

        return retcode, result
