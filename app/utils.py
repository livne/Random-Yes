import GeoIP
from country_langs import country_langs
from language_names import language_names
from country_names import country_names
from user_names import us
from django.utils.translation import ugettext_lazy as _
from string import strip
from random import choice, sample
from app.models import CustomUser
from app.country_names import country_names

MAX_RECIPIENTS_AMOUNT=5

def geo_country(request):
    try:
        ip = request.META['REMOTE_ADDR']
    except KeyError:
        ip = "0.0.0.0"
    gi = GeoIP.new(GeoIP.GEOIP_STANDARD)
    return gi.country_code_by_addr(ip).lower()

def country_lang(country_code):
    return country_all_langs(country_code).split(';')[0].strip() # take the first language

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

def random_user_name(country_code):
    # surname and given name
    return [choice(us[0]),choice(us[1])]

def random_recipients(sender_id, requested_amount, countries=None, language=None, gender=None, age=None, keywords=None):
    # is_active=True: login + sent once.
    # cron - after 2 days with no login set is_active False.
    # FIXME: cache user list for 10 min.
    potential_recipients = CustomUser.objects.filter(is_active__exact=True).exclude(pk=sender_id).exclude(karma=0)
    potential_group_size=len(potential_recipients)
    if potential_group_size == 0:
        potential_recipients = CustomUser.objects.filter(is_active__exact=True).exclude(pk=sender_id)
        potential_group_size=len(potential_recipients)
    n = min(MAX_RECIPIENTS_AMOUNT, requested_amount, potential_group_size)
    return sample(potential_recipients, n)

def initial_subject(user):
    return 'Hello from ' + country_names[user.country]

def initial_body(user):
    body = 'Hi! My name is ' + user.first_name + '. '
    body += 'I would like that we write to each other. '
    body += 'Few details about me: I am '
    if user.gender:
        if user.gender is 'f':
            gender = 'female'
        else:
            gender = 'male'
        body += 'a ' + gender + ', '
    if user.age:
        body += str(user.age) + ' years old, '
    body += 'from ' + country_names[user.country]
    body += 'and I would be happy to learn few things about you.'
    return body

