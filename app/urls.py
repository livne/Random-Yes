from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^status/$', 'randomyes.app.views.status'),
    # uuid4
    # xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx
    # hexadecimal digits x
    # 8, 9, a, or b for y
    (r'^inbox/(?P<uuid>[0-9,a-f]{8}-[0-9,a-f]{4}-4[0-9,a-f]{3}-[8,9,a,b]{1}[0-9,a-f]{3}-[0-9,a-f]{12})/$', 'randomyes.app.views.inbox'),
)

