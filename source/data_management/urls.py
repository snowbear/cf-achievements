from django.conf.urls import patterns, url

from data_management import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)
