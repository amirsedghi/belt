from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^appointments$', views.appointments),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^add$', views.add),
    url(r'^edit/(?P<id>\d+)$', views.edit),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^update/(?P<id>\d+)$', views.update),
]
