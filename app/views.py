from django.shortcuts import render_to_response
from app.auth_backends import CustomUserModelBackend 
from django import template
from django.utils.translation import ugettext_lazy as _
from app.models import CustomUser
from django.contrib.auth import authenticate, login


def status(request):
    if request.user.is_authenticated():
      output = _('Authenticated')
    else:
      output = _('Not authenticated')
    return render_to_response('app/welcome.html', {'error_message': output}, context_instance=template.RequestContext(request))

def inbox(request, uuid):
    user = authenticate(token=uuid)
    if user is not None:
        if user.is_active:
            login(request, user)
    return render_to_response('app/welcome.html', {'error_message': uuid}, context_instance=template.RequestContext(request))
