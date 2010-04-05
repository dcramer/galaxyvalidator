from coffin.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    (r'^media/(?:\d+/)?(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    (r'^favicon.ico$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'path': '/images/favicon.ico'}),

    #url(r'^robots\.txt$', 'coffin.views.generic.simple.direct_to_template', {'template': 'robots.txt', 'mimetype': 'text/plain'}),

    (r'^admin/(.*)', admin.site.root),

    url(r'^', include('galaxyvalidator.validator.urls')),
)
