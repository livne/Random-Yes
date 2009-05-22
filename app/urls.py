from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^status/$', 'randomyes.app.views.status'),
    (r'^login/(?P<token>[0-9,a-z,A-Z]{30})/$', 'randomyes.app.views.rylogin'),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'app/welcome.html'}),
    (r'^new/$', 'randomyes.app.views.new'),
    (r'^recipients/$', 'randomyes.app.views.recipients'),
    (r'^preferences/$', 'randomyes.app.views.preferences'),
    (r'^welcome/$', 'randomyes.app.views.welcome'),
    (r'^debug/$', 'randomyes.app.views.debug'),
)

