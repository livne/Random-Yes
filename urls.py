# NEW:
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
)


#from django.conf.urls.defaults import *

#urlpatterns = patterns('',
    # Example:
    # (r'^randomyes/', include('randomyes.foo.urls')),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
#)
