from django.conf.urls import patterns, url

from data_management import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^contests-update$', views.load_contests, name='load-contests'),
    url(r'^contests-save$', views.save_contest, name='contests-save'),
    url(r'^update-achievement/(?P<achievementId>\d+)$', views.update_achievement, name='update-achievement'),
    url(r'^save-contest-achievement$', views.save_contest_achievement, name='save-contest-achievement'),
    url(r'^update-ratings$', views.ratings_update, name='ratings-update'),
    url(r'^save-ratings$', views.ratings_save, name='ratings-save'),
)
