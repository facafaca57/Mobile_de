from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^load/$', views.load, name='load'),
    url(r'^add/$', views.add, name='add'),
    url(r'^search/$', views.search, name='search'),
]