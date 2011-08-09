import functools

class APIExecutor(object):

    wrappers = []

    def __init__(self, target):
        f = target
        for wrapper in self.wrappers:
            target_pref = getattr(target, wrapper.prop, None)
            if target_pref is None: target_pref = getattr(wrapper, 'default', None)
            if target_pref:
                f = wrapper(f)
                functools.update_wrapper(f, target)

        self.f = f

    def __call__(self, *args, **kw):
        return self.f(*args, **kw)

class Application(object):
    mapper = None
    APIExecutor = APIExecutor

    def __init__(self):
        self.on_startup = []
        self.on_shutdown = []

    def connect(self, methods, prefix=''):
        if isinstance(methods, (list, tuple)):
            for m in methods:
                self.mapper[prefix + m.__name__] = self.APIExecutor(m)
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



