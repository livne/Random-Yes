from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'', include('randomyes.app.urls')),
    (r'^messages/', include('messages.urls')),
)
