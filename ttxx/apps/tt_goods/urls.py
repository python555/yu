# coding:utf8
from django.conf.urls import url

from tt_goods import views

urlpatterns=[
	url('^test$',views.test),
	url('^$', views.index),  #127.0.0.1:8000  ==>直接进入首页

]