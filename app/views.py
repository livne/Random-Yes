from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from app.auth_backends import CustomUserModelBackend 
from django import template
from django.utils.translation import ugettext_lazy as _
from app.models import CustomUser
from django.contrib.auth import authenticate, login
from string import letters, digits
from random import choice
from utils import geo_country, country_lang, language_name, country_name

def status(request):
    if request.user.is_authenticated():
      output = _('Authenticated')
    else:
      output = _('Not authenticated')
    return render_to_response('app/welcome.html', {'error_message': output}, context_instance=template.RequestContext(request))

def inbox(request, token):
    user = authenticate(token=token)
    if user is not None:
        if user.is_active:
            login(request, user)
        if user.country == 'xx': # undefined
            user.country = geo_country(request)
            user.language = country_lang(user.country)
    return render_to_response('app/welcome.html', {'language': language_name(user.language), 'country': country_name(user.country)}, context_instance=template.RequestContext(request))

def new(request):
    token=''.join(choice(letters+digits) for i in xrange(30))
    return HttpResponseRedirect('/go/inbox/%s' % token)

