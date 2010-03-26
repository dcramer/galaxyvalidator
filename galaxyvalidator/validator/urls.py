from coffin.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='validator'),
)
