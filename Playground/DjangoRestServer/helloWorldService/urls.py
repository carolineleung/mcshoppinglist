import os
import re
from django.conf.urls.defaults import patterns, include
from django.contrib import admin
import settings
import shoppinglists

# FIX for tests: AttributeError: 'module' object has no attribute 'handler500'
# http://code.djangoproject.com/ticket/11013#comment:1
# from django.conf.urls.defaults import patterns, include, handler500, handler404
from django.conf.urls.defaults import patterns, include, handler500, handler404

admin.autodiscover()

urlpatterns = patterns('',
    (r'^api/v1/shoppinglists/?', include('shoppinglists.urls')),
    #(r'^admin/', include('admin.site.urls')),
    # TODO make it /editor or something
    (r'^/?', include('shoppinglisteditor.urls')),
    #    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

if settings.DEBUG:
    # TODO This is a workaround to serve static files when debugging (running by manage.py serve)
    # http://docs.djangoproject.com/en/1.2/howto/static-files/
    fs_path = '{0}'.format(os.path.dirname(__file__))
    # TODO How can we DRY /static ? pre-compiling regex won't work due to <path> var
    #static_doc_re = re.compile('^{0}/(?P<path>.*)$'.format(settings.STATIC_DOC_ROOT))
    urlpatterns += patterns('',
        ('^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': fs_path}),)
