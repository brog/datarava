from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic.simple import direct_to_template
admin.autodiscover()

urlpatterns = patterns('',
    ( r'^resources/(?P<path>.*)$',
	      'django.views.static.serve',
	      { 'document_root': settings.MEDIA_ROOT } ),
    url(r'^sleeprecords/$', 'sleeprecord.views.index'),
    url(r'^sleeprecords/updatemydata/$', 'sleeprecord.views.updatemydata'),
    url(r'', include('social_auth.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'datarava/login.html'}),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'datarava/login.html'}), 
    (r'^$', direct_to_template, {'template': 'datarava/index.html'}),
     url(r'^withings/request_token_ready/$', 'withings.views.request_token_ready'),
     url(r'^withings/request_token/$', 'withings.views.request_token'),  
    url(r'^accounts/$', 'accounts.views.index'),  


    # Examples:
    # url(r'^$', 'datarav.views.home', name='home'),
    # url(r'^datarav/', include('datarav.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
