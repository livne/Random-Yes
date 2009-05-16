from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import login, logout

def myview(request):
    if request.user.is_authenticated():
      return HttpResponseRedirect('/loggedin/')
    else:
      if request.POST:
        authd = login(request)
        authd = request.user.is_authenticated()
        if authd:
          return HttpResponseRedirect('/loggedin/')
      logged_in = login(request)
      return logged_in
