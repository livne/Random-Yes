from django.conf.urls.defaults import *

urlpatterns = patterns('',
#    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^$', 'randomyes.app.views.myview'),
#    (r'^(?P<tab_name>[A-Z,a-z,0-9,\-,\_]+)/$', 'tabnu.app.views.tab'),
)

