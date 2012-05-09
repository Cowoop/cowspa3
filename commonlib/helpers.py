try:
    import builtins
except:
    import __builtin__ as builtins # Python 2.x compatibility

import datetime
import itertools
import collections
import base64, random, hashlib
import dateutil.parser
import simplejson

random_key_gen = None

def push_to_builtins(name, o):
    setattr(builtins, name, o)

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

def date4human(date_or_iso):
    if not isinstance(date_or_iso, (datetime.date, datetime.datetime)):
        date_or_iso = iso2date(date_or_iso)
    return date_or_iso.strftime("%b %d, %Y")

def time4human(date_or_iso):
    if not isinstance(date_or_iso, (datetime.date, datetime.datetime)):
        date_or_iso = iso2datetime(date_or_iso)
    return date_or_iso.strftime("%I:%M%p")

def datetime4human(date):
    return date.strftime("%b %d, %Y %I:%M%p")

def iso2date(iso):
    if isinstance(iso, datetime.datetime): return iso.date()
    elif isinstance(iso, datetime.date): return iso
    return datetime.datetime.strptime(iso[0:10], "%Y-%m-%d").date() if iso else None

def iso2datetime(iso):
    if isinstance(iso, datetime.datetime):
        return iso
    return dateutil.parser.parse(iso) if iso else None

def sortngroupby(iterable, keyfn, reverse=False):
    l = sorted(iterable, key=keyfn)
    return itertools.groupby(l, keyfn)

def html2pdf(input_file ,output_file):
    import wkhtmltox
    pdf = wkhtmltox.Pdf()
    pdf.set_global_setting('out', output_file)
    pdf.add_page({'page': input_file})
    pdf.convert()
    return True
