import datetime
import collections
import base64, random, hashlib
import wkhtmltox
import simplejson
from flask import current_app

random_key_gen = None

class odict(dict):
    def __getattr__(self, attr):
        return self[attr]

class RandomKeyFactory(object):
   def __init__(self, s):
       self.random_choices = (s[:2], s[2:4], s[4:6], s[6:8], s[8:10], s[10:12], s[12:14])
   def __call__(self):
       return base64.b64encode(hashlib.sha256(str(random.getrandbits(256))).digest(), \
           random.choice(self.random_choices)).rstrip('==')

callable = lambda o: isinstance(o, collections.Callable)

def encrypt(s, salt=''):
    h = hashlib.sha256()
    h.update(s+salt)
    return h.hexdigest()

class Constants(object):
    """
    >>> class Statuses(Constants):
    >>>     names = ['open', 'pending', 'closed']

    >>> statuses = Statuses()
    >>> statuses.open
    0
    >>> statuses.rev(0)
    'open'
    """
    names = []
    def __init__(self):
        self.nt = collections.namedtuple(self.__class__.__name__, ' '.join(self.names))._make(range(len(self.names)))
    def __getattr__(self, name):
        return getattr(self.nt, name)
    def rev(self, n):
        return self.nt._fields[n]

def setdefaultencoding():
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

def html2pdf(input_file ,output_file):
    pdf = wkhtmltox.Pdf()
    pdf.set_global_setting('out', output_file)
    pdf.add_page({'page': input_file})
    pdf.convert()
    return True

def date4human(date):
    return date.strftime("%b %d, %Y")

def datetime4human(date):
    return date.strftime("%b %d, %Y %I:%M%p")

def iso2date(iso):
    return datetime.datetime.strptime(iso, "%Y-%m-%d").date()

def iso2datetime(iso):
    return datetime.datetime.strptime(iso, "%Y-%m-%dT%H:%M:%S").date()

def jsonify(obj):
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date) else None
    return current_app.response_class(simplejson.dumps(obj, use_decimal=True, default=dthandler), mimetype='application/json')
