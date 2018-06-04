# coding:utf8
from django.conf.urls import url

from tt_user import views

urlpatterns=[
	
	# url("^register$",views.register),
	url('^register$',views.RegisterView.as_view()),
	url('^active/(.+)$',views.active),
]