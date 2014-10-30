from django.conf.urls import patterns, url

from achievements import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^profile/(?P<handle>.+)$', views.profile, name='profile'),
    url(r'^contest/(?P<contestId>\d+)$', views.contest, name='contest'),
    url(r'^achievement/(?P<achievementId>\d+)$', views.achievement, name='achievement'),
    url(r'^search-user$', views.search_user, name='search_user'),
)
