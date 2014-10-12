from django.conf.urls import patterns, url

from data_management import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^contests-update$', views.load_contests, name='load-contests'),
    url(r'^contests-save$', views.save_contest, name='contests-save'),
)
