from coffin.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^', include('galaxyvalidator.validator')),
)
