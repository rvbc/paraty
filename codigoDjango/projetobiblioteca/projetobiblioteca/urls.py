from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^biblioteca/$', 'biblioteca.views.home', name='home'),
    # url(r'^projetobiblioteca/', include('projetobiblioteca.foo.urls')),
    url(r'^biblioteca/suggestion', 'biblioteca.views.add_suggestion'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
