from coffin.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='validator'),
    url(r'^results/(?P<result_id>[A-Z0-9a-z]{32})/$', views.results, name='validator.results'),
)
