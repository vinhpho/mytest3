from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^createuser$', views.createuser),
    url(r'^login$', views.login),
    url(r'^user_dashboard$', views.user_dashboard),
    url(r'^user/(?P<id>\d+)$', views.show_user),
    url(r'^nonuser/(?P<id>\d+)$', views.show_non_user),
    url(r'^add_friend/(?P<id>\d+)$', views.add_friend),
    url(r'^remove_friend/(?P<id>\d+)$', views.remove_friend),
    url(r'^logout$', views.logout),
]
