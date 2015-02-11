from django.conf.urls import patterns, url

from leagues import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view()),
    url(r'^start$', views.start, name='start'),
    url(r'^ready$', views.ready, name='ready'),
)