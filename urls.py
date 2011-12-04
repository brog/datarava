from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    ( r'^resources/(?P<path>.*)$',
	      'django.views.static.serve',
	      { 'document_root': settings.MEDIA_ROOT } ),
    url(r'^sleeprecords/$', 'sleeprecord.views.index'),
    url(r'^sleeprecords/updatemydata/user/(\d+)/$', 'sleeprecord.views.updatemydata'),
   url(r'', include('social_auth.urls')),
#    url(r'^logout/$', logout, name='logout'),



    # Examples:
    # url(r'^$', 'datarav.views.home', name='home'),
    # url(r'^datarav/', include('datarav.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
