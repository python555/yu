# coding:utf8
from django.contrib.auth.decorators import login_required
from django.views.generic import View

#django中对于类试图添加装饰器的方式之一,底层封装类好几个试图
class LoginRequiredView(View):  #验证封装重写,缺点:只能继承View一个类
	@classmethod
	def as_view(cls,**initkwargs):
		func=super().as_view(**initkwargs)
		return login_required(func)
	
#多继承方案,添加装饰器方式之一(推荐使用)
class LoginRequiredViewMixin(object):
	@classmethod
	def as_view(cls,**initkwargs):
		func=super().as_view(**initkwargs)
		return login_required(func)