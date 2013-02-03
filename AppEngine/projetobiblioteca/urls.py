from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
	url(r'^$', 'biblioteca.views.home'),
    url(r'^login', 'biblioteca.views.login'),
    url(r'^logout', 'biblioteca.views.logout'),
    url(r'^suggestion/$', 'biblioteca.views.suggestion'),
    url(r'^books/$', 'biblioteca.views.books'),
    url(r'^books/search', 'biblioteca.views.search'),
    url(r'^table/$', 'biblioteca.views.table'),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include('admin.site.urls')),
)
