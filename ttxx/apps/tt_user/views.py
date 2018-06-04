import re

from django.conf import settings
from django.contrib.auth import authenticate,login
from django.core.mail import send_mail
from django.http import HttpResponse, response
from django.http import JsonResponse
from django.shortcuts import render, redirect
from itsdangerous import  TimedJSONWebSignatureSerializer as Serializer12, SignatureExpired
# Create your views here.
from django.views.generic import View
from celery_tasks.tasks import send_user_active

# def register(request):  #用于get请求
# 	'''
# 	展示注册页面
# 	:param request:
# 	:return:
# 	'''
# 	if request.method=='GET':
# 		return render(request,"register.html")
# 	elif request.method=='POST':
# 		#处理注册
# 		pass
# def registerHandle(request):  #用于post请求
# 	'''
# 	处理注册
# 	:param request:
# 	:return:
# 	'''
# 	pass
from tt_user.models import User


class RegisterView(View): #类视图是内部封装的方法,继承View,好处:可以增加_init_初始化对共有属性进行封装
	def get(self,request):  #get,post是固定用法,底层封装默认小写
		return render(request, "register.html",{'title':'注册处理'})
	def post(self,request):
		#接受数据
		dict=request.POST
		uname=dict.get('user_name')
		upwd=dict.get('pwd')
		cpwd=dict.get('cpwd')
		uemail=dict.get('email')
		uallow=dict.get('allow')
		
		#判断是否同意协议
		if not uallow:
			return render(request,'register.html',{'err_msg':'请同意协议'})
		
		#判断数据是否存在
		if not all([uname,upwd,cpwd,uemail]):  #其中一个不存在返回None,都存在返回Ture
			return render(request,'register.html',{'err_msg':'请将信息填写完整'})
			
		#用户错误提示的数据
		context={
			'uname':uname,
			'upwd':upwd,
			'cpwd':cpwd,
			'email':uemail,
			'err_msg':'',
			'title':'注册处理'
		}
		
		#判断两次密码是否一致
		if upwd!=cpwd:
			context['err_msg']='两次密码输入不一致'
			return render(request,'register.html',context)
		
		#判断用户名是否存在
		if User.objects.filter(username=uname).count()>0:
			context['err_msg'] = '用户名已经存在'
			return render(request,'register.html',context)
		
		#判断邮箱格式是否正确
		if not re.match(r'[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}',uemail):
			context['err_msg'] = '邮箱格式不正确'
			return render(request,'register.html',context)

		
		#判断邮箱是否存在
		if User.objects.filter(email=uemail).count()>0:
			context['err_msg'] = '邮箱已经存在'
			return render(request,'register.html',context)
		
		#处理(创建用户对象)
		user=User.objects.create_user(uname,uemail,upwd)   #此格式User.objects.create_user()用于用户名,邮箱,密码
		user.is_active=False  #邮件激活状态
		user.save()
		
		# #将帐号信息进行加密
		# serializer=Serializer12(settings.SECRET_KEY,60*60*2) #设置加密
		# value=serializer.dumps({'id':user.id})  #dumps为加密,为bytes类型
		# value=value.decode()#转成字符串,用于拼接地址
		#
		# #向用户发送邮件
		# # msg='<a href="htthp://127.0.0.1:8000/user/active/%d">点击激活</a>'%user_id
		# msg='<a href="htthp://127.0.0.1:8000/user/active/%s">点击激活</a>'%value
		# send_mail('天天先鲜激活','',settings.EMALL_FROM,[uemail],html_message=msg) #其他参数不写,会自动去setting中找数据
		
		#使用celery发送激活邮件
		send_user_active.delay(user)   #delay()功能---会把参数和任务扔给celery
		
		#给出响应
		return HttpResponse('请在两个小时内---接受邮件---激活账户')

def active(request,value):  #接受参数:request和加密的字符串,可知道用户对应的id和验证码是否过期
	serializer=Serializer12(settings.SECRET_KEY)  #解密不需要时间
	try:
		#解析用户编号
		dict=serializer.loads(value)#loads为解密,转成json类型,只是像字典
		userid=dict.get('id')
		#激活账户
		user=User.objects.get(pk=userid)#根据userid拿到用户id
		user.is_active=True  #修改激活状态
		user.save()
		
		# return HttpResponse(dict.get('id'))
		#转到登录页面
		return redirect('/user/login')
	except SignatureExpired as e: #机密失败抛出异常
		print('激活链接已经过期')
		
	
def exists(request):
	'''
	判断用户名或邮箱是否存在
	:return:
	'''''
	uname=request.GET.get('uname')
	if uname is not None:
		result=User.objects.filter(username=uname).count()
	return JsonResponse({'result':result})


class LoginView(View):
	def get(self,request):
		uname=request.COOKIES.get('uname','') #没有uname时,会用空字符串,不传入空字符串就会会显示None
		return render(request,'login.html',{'title':'登录','uname':uname})
	def post(self,request):
		#接受数据
		dict =request.POST
		uname=dict.get('username')
		pwd=dict.get('pwd')
		remember=dict.get('remember')
		
		#构造返回值
		context={
			'title':'登录处理',
			'uname':uname,
			'pwd':pwd,
			'err_msg': '请填写完整信息',
		}
		
		#验证是否填写数据
		if not all([uname,pwd]):
			return render(request,'login.html',context)
		
		#验证验证用户名,密码是否正确
		user=authenticate(username=uname,password=pwd) #需要关键字参数
		if user is None:
			context['err_msg']='用户名或密码错误'
			return render(request,'login.html',context)
		
		#判断用户是否激活
		if not user.is_active:
			context['err_msg']='请到邮箱中激活账户'
			return render(request,'login.html',context)
		
		#记录状态
		login(request,user)
		
		#是否勾选记住用户名操作,存入cookie中,没勾选会删除
		if remember is not None:
			response.set_cookie('uname',uname,expires=60*60*24*7)
		else:
			response.delete_cookie('uname')
		
		#转向用户中心
		return redirect('/user/info')