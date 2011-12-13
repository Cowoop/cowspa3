import sys
import traceback
import commonlib.helpers

# * Resource and Collection *
# Structures that helps clean organize Resource/Collection APIs.
# These objects may help publisher to introspect resource/collection and decide on exposing APIs
# Apart from this these structures do not play any significant role.

class Resource(object):
    """
    function with name that starts with _ will be considered as internal apis
    """
    def __init__(self):
        self.exposed_funcs = {}
    def __setattr__(self, name, f):
        if name[0] is not '_' and commonlib.helpers.callable(f):
            self.exposed_funcs[name] = f
        object.__setattr__(self, name, f)

class Collection(Resource):
    """
    Currently there is no implementation difference between Resource and Collection.
    In future there might be a few. So keeping Collection as independent class.
    """

class APIExecutor(object):

    wrappers = []

    def __init__(self, target):
        f = target
        for wrapper in self.wrappers:
            target_pref = getattr(target, wrapper.prop, None)
            if target_pref is None: target_pref = getattr(wrapper, 'default', None)
            if target_pref:
                f = wrapper(f)
        self.f = f

    def __call__(self, *args, **kw):
        try:
            return self.f(*args, **kw)
        except Exception as err:
            traceback.print_exc(file=sys.stdout)
            raise

class Application(object):
    mapper = None
    APIExecutor = APIExecutor
    context_setter = lambda x: None

    def __init__(self):
        self.on_startup = []
        self.on_shutdown = []

    def connect(self, methods, prefix=''):
        if isinstance(methods, (list, tuple)):
            for m in methods:
                self.mapper[prefix + m.__name__] = self.APIExecutor(m)
        elif isinstance(methods, (Resource, Collection)):
            for name, f in methods.exposed_funcs.items():
                self.mapper[prefix + '.' + name] = self.APIExecutor(f)
        else:
            if not prefix:
                prefix = methods.__name__
            self.mapper[prefix] = self.APIExecutor(methods)

    def startup(self):
        for f in self.on_startup:
            f()
            print self.name, ':startup::', f.__func__.__module__, '.', f.__name__

    def shutdown(self):
        # sys.atexit
        for f in self.on_shutdown:
            f()

    def tr_start(self):
        for f in self.on_tr_start:
            f()

    def tr_complete(self):
        for f in self.on_tr_complete:
            f()

    def tr_abort(self):
        for f in self.on_tr_abort:
            f()
    def dispatch(self, auth_token, params):
        """
        params: eg. {"jsonrpc": "2.0", "method": methodname, "params": params, "id": 1}
        """
        self.tr_start()
        set_context_successful = False
        data = {}
        if auth_token:
            try:
                self.context_setter(auth_token)
                set_context_successful = True
            except Exception, err:
                print (err)
                self.tr_abort()
        if (auth_token and set_context_successful) or not auth_token:
            data = self.mapper(params) # Assumption this does not raise exception
        # else return jsonrpc unauthenticated code
        self.tr_complete()
        return data
