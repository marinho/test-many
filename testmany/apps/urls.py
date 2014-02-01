from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.views',
    url(r'^$', "index"),
    url(r'^projects\.json$', "projects_json"),
)

