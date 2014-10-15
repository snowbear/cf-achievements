from django.conf.urls import patterns, url

from achievements import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^profile/(?P<handle>.+)$', views.profile, name='profile'),
)
