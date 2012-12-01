from django.conf.urls import patterns, include, url
from biblioteca import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('biblioteca.views',
    # Examples:
    url(r'^biblioteca/$', 'home', name='home'),
    url(r'^biblioteca/suggestion/$', 'suggestion'),
    url(r'^biblioteca/books/$', 'books'),
    url(r'^biblioteca/books/search', views.search),
    url(r'^biblioteca/books/export', views.export),
    url(r'^biblioteca/suggestion/add', views.add_suggestion),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
