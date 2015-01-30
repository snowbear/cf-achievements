from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('achievements.urls', namespace="achievements")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^data-management/', include('data_management.urls', namespace="data")),
)
