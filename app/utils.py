import GeoIP
from country_langs import country_langs
from language_names import language_names
from country_names import country_names
from django.utils.translation import ugettext_lazy as _
from string import strip

def geo_country(request):
    try:
        ip = request.META['REMOTE_ADDR']
    except KeyError:
        ip = "0.0.0.0"
    gi = GeoIP.new(GeoIP.GEOIP_STANDARD)
    return gi.country_code_by_addr(ip).lower()

def country_lang(country_code):
    return country_all_langs(country_code).split(';')[0] # take the first language

def country_all_langs(country_code):
    try:
        langs = country_langs[country_code]
    except KeyError:
        langs = 'en'
    return langs

def country_name(country_code):
    try:
        name = country_names[country_code]
    except KeyError:
        name = _('Invalid country code: ')+unicode(country_code)
    return name

def language_name(language_code):
    try:
        name = language_names[strip(language_code.lower())]
    except KeyError:
        name = _('Invalid language code: ')+unicode(language_code)
    return name

