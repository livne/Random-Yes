from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from app.auth_backends import CustomUserModelBackend 
from django import template
from django.utils.translation import ugettext_lazy as _
from app.models import CustomUser, PreferencesForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from string import letters, digits
from random import choice
from utils import geo_country, country_lang, language_name, country_name, random_user_name, random_recipients

def welcome(request):
    return render_to_response('app/welcome.html', context_instance=template.RequestContext(request))

def debug(request):
    users_list = CustomUser.objects.all()
    return render_to_response('app/debug.html', {'users': users_list}, context_instance=template.RequestContext(request))

def status(request):
    return render_to_response('app/status.html', context_instance=template.RequestContext(request))

def rylogin(request, token):
    user = authenticate(token=token)
    if user is not None:
        login(request, user)
        if user.country == 'xx': # undefined
            user.country = geo_country(request)
            user.language = country_lang(user.country)
            name = random_user_name(user.country)
            user.last_name=name[0]
            user.first_name=name[1]
            user.is_active=True
            user.save()
        return recipients(request)
    else:
        return HttpResponseRedirect('/welcome/')

def new(request):
    token=''.join(choice(letters+digits) for i in xrange(30))
    return HttpResponseRedirect('/login/%s' % token)

def recipients(request):
    user = request.user 
    if not user.is_authenticated():
       HttpResponseRedirect('/')
    for r in user.recipients.all():
        user.recipients.remove(r)
    recipients = random_recipients(user.id, user.recipients_amount)
    for r in recipients:
        user.recipients.add(r)
    user.save()
    try:
        next = request.META['HTTP_REFERER']
    except:
        next = '/messages/inbox/'
    return HttpResponseRedirect(next)
recipients = login_required(recipients)

def preferences(request):
    user = request.user
    form = PreferencesForm(data=request.POST or None, instance=user)
    if form.is_valid():
        form.save()
    return render_to_response('app/preferences.html', {'form': form}, context_instance=template.RequestContext(request))
preferences = login_required(preferences)

