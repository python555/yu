# coding:utf8
from django.conf.urls import url

from . import views

urlpatterns=[
	
	# url("^register$",views.register),
	url('^register$',views.RegisterView.as_view()),
	url('^active/(.+)$',views.active),
	url('^exists$',views.exists),
	url('^login$',views.LoginView.as_view()),  #有get和post,需要调as_view
]