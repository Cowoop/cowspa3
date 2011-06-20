import bases.errors as errors

class Application(object):
    def startup(self):
        pass
    def shutdown(self):
        pass

class Collection(object):
    pass

class Resource(object):
    _get_methods = []
    _set_methods = []

class RestMapper(object):

    def connect(self, path, func):
        pass

    def connect_collection(self, path, collection):
        pass

    def connect_resource(self, path, resource):
        pass

class Dispatcher(object):

    def __init__(self, tree, pg_provider, comps=[]):
        self.comps = comps
        self.tree = tree
        self.pg_provider = pg_provider

    def __getattr__(self, name):
        comps = object.__getattribute__(self, 'comps') + [name]
        tree = object.__getattribute__(self, 'tree')
        pg_provider = object.__getattribute__(self, 'pg_provider')
        dispatcher = Dispatcher(tree, pg_provider, comps)
        return dispatcher

    def execute(self, args, kw):
        f = self.tree
        for comp in self.comps:
            f = getattr(f, comp)

        perms_needed = getattr(f, 'perms', None)
        if perms_needed is not None:
            helpers.perm_checker(context, perms_needed)

        return f(*args, **kw)

    def __call__(self, *args, **kw):
        retcode = errors.success
        result = None
        try:
            self.pg_provider.tr_start()
            result = self.execute(args, kw)
            self.pg_provider.tr_complete()
        except Exception as err:
            print(err)
            self.pg_provider.tr_abort()

        return retcode, result
