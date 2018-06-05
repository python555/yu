# coding:utf8
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns=[

	# url("^register$",views.register),
	url('^register$',views.RegisterView.as_view()),
	url('^active/(.+)$',views.active),
	url('^exists$',views.exists),
	url('^login$',views.LoginView.as_view()),  #有get和post,需要调as_view
	url('^logout$',views.logout_user),
	url('^info$', views.info),
	url('^order$', views.order),
	url('^site$', views.SiteView.as_view()),
	
	#url('^site$', login_required(views.SiteView.as_view())),  #装饰器验证格式和wrapper(fun1)的格式一样,但一般不这样使用
	#在工具文件夹下定义一个类,重写as_view,并返传给login_required(参数)返回
	
	url('^area$',views.area),
]



