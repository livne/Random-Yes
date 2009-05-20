from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^status/$', 'randomyes.app.views.status'),
    (r'^inbox/(?P<uuid>[A-Z,a-z,0-9,\-]+)/$', 'randomyes.app.views.inbox'),
)

