import pycountry

resource_types = ['room', 'tariff', 'phone', 'printer', 'custom','hotdesk', 'calendar', 'other']
languages = ['English', 'German']
themes = ['default', 'clean', 'hub']
language_map = dict((lang.alpha2, lang.name) for lang in pycountry.languages if hasattr(lang, 'alpha2'))
language_map_rev = dict((lang.name, lang.alpha2) for lang in pycountry.languages if hasattr(lang, 'alpha2'))
countries = [country.name.encode("utf-8") for country in list(pycountry.countries)]
currencies = [currency for currency in list(pycountry.currencies)]
