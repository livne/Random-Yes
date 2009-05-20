from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^status/$', 'randomyes.app.views.status'),
    (r'^inbox/(?P<token>[0-9,a-z,A-Z]{30})/$', 'randomyes.app.views.inbox'),
)

