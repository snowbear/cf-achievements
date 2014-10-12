from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cf_achievements.views.home', name='home'),
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^achievements/', include('achievements.urls', namespace="achievements")),
    url(r'^data-management/', include('data_management.urls', namespace="data")),

    url(r'^admin/', include(admin.site.urls)),
)
