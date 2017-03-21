# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^(?P<slug>[-\w]+)/$', views.portfolio_detail, name='detail'),
]