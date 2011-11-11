import pycountry
import glob
import os

resource_types = [dict(name='room', label='Room'), dict(name='tariff', label='Tariff'), dict(name='phone', label='Phone'), dict(name='printer', label='Printer'), dict(name='hotdesk', label='Hotdesk'), dict(name='other', label='Other')]

language_map = dict((lang.name, lang.alpha2) for lang in pycountry.languages if hasattr(lang, 'alpha2'))
languages = [dict(label='English',name=language_map['English']), dict(label='German', name=language_map['German'])]

countries = [dict(label=country.name ,name=country.numeric) for country in list(pycountry.countries)]
countries_map = dict((country.numeric,country.name) for country in list(pycountry.countries))

currencies = [dict(name=currency.letter ,label=currency.name) for currency in list(pycountry.currencies)]

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
