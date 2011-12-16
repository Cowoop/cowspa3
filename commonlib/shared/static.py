import pycountry
import glob
import os
from operator import itemgetter
from pytz import common_timezones
from babel import Locale, localedata

#TODO : Static list of resources won't work for long. Need a way for users to
#       create own resource types apart from system default
resource_types = [dict(name='room', label='Room'), dict(name='phone', label='Phone'), 
        dict(name='printer', label='Printer'), dict(name='other', label='Other')]

#language_map = dict((lang.name, lang.alpha2) for lang in pycountry.languages if hasattr(lang, 'alpha2'))
#languages = [dict(label='English',name=language_map['English']), dict(label='German', name=language_map['German'])]

languages = [dict(name=locale, label=Locale.parse(locale).english_name) for
            locale in [l for l in localedata.list() if Locale.parse(l).english_name is not None]]
languages.sort(key=itemgetter('label'))

countries = [dict(label=country.name ,name=country.numeric) for country in list(pycountry.countries)]
countries_map = dict((country.numeric,country.name) for country in list(pycountry.countries))

currencies = [dict(name=currency.letter ,label=currency.name) for currency in list(pycountry.currencies)]

timezones = [dict(name=el,label=el) for el in common_timezones]

themeroot = 'fe/src/themes'
themedirs = [os.path.basename(name) for name in glob.glob(themeroot + '/*') if os.path.isdir(name)]
themedirs.remove('base')

def themedict(themedir):
    manifest_path = os.path.join(themeroot, themedir, 'manifest')
    if not os.path.isfile(manifest_path):
        raise Exception("File does not exist (or not a file): %s" % manifest_path)
    manifest = {}
    execfile(manifest_path, {}, manifest)
    return dict(name = os.path.basename(themedir), label = manifest['name'])

themes = [themedict(path) for path in themedirs]
