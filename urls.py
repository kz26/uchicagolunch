from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'site_main.views.home'),
    url(r'^faq/$', direct_to_template, {'template': 'faq.html'}, name="faq"),
    url(r'^tos/$', direct_to_template, {'template': 'terms.html'}, name="terms"),
    url(r'^favicon.ico/$', redirect_to, {'url': 'http://static.uchicagolunch.com/favicon.ico'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
