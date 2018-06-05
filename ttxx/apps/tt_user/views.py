import re

from django.conf import settings
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse, response
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django_redis import get_redis_connection
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired
# Create your views here.
from django.views.generic import View
from celery_tasks.tasks import send_user_active
from tt_goods.models import GoodsSKU
from utils.views import LoginRequiredView,LoginRequiredViewMixin

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
from tt_user.models import User, Address, AreaInfo


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

		#
		# #判断邮箱是否存在
		# if User.objects.filter(email=uemail).count()>0:
		# 	context['err_msg'] = '邮箱已经存在'
		# 	return render(request,'register.html',context)

		#处理(创建用户对象)
		user=User.objects.create_user(uname,uemail,upwd)   #此格式User.objects.create_user()用于用户名,邮箱,密码
		user.is_active=False  #邮件激活状态
		print(type(uemail))
		print(type(upwd))

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
		# send_user_active.delay(user)  #不能一起传过去,因为不能将两个字符串同时序列化
		
		send_user_active.delay(uemail)   #delay()功能---会把参数和任务扔给celery
	
		send_user_active.delay(upwd)


		#给出响应
		return HttpResponse('请在两个小时内---接受邮件---激活账户')

def active(request,value):  #接受参数:request和加密的字符串,可知道用户对应的id和验证码是否过期
	serializer=TimedJSONWebSignatureSerializer(settings.SECRET_KEY)  #解密不需要时间
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
		return HttpResponse('激活链接已经过期')


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
			'err_msg': '请填写完成信息',
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
		
		# 转向用户中心
		next_url=request.GET.get('next','/user/info') #登录后,转到在哪个网页登录的地址,没有就转到默认地址:个人中心
		response=redirect(next_url)

		#是否勾选记住用户名操作,存入cookie中,没勾选会删除
		if remember is not None:
			response.set_cookie('uname',uname,expires=60*60*24*7)
		else:
			response.delete_cookie('uname')

		
		return response
	
def logout_user(request):  #起的函数名不能和底层函数冲突
	#用户退出,原理就是把状态保持的session等删除
	logout(request)
	return redirect('user/login')

@login_required  #验证登录 ,需要在settings另外添加配置项
def info(request):  #用户中心
	#被装饰器登录验证替代,可在模板中使用验证
	# if request.user.is_authenticated(): #django验证系统,判断用户是否登录
	# 	pass
	# else:
	# 	return redirect('/user/login')
	
	#从redis中读取浏览记录
	#浏览记录在商品的详情页试图中添加(后面再做)
	#获取redis服务器的连接
	client=get_redis_connection()
	history_list=client.lrange('history%d'%request.user.id,0,-1)  #没有返回空列表
	history_list2=[]
	if history_list:
		for good_id1 in history_list:
			history_list2.append(GoodsSKU.objects.get(pk=good_id1))
	
	#查询默认收货地址
	addr=request.user.address_set.all().filter(isDefault=True)
	if addr:
		addr=addr[0]
	else:
		addr=''
	
	context={
		'title':'个人信息',
		'addr':addr,
		'history':history_list2
	}
	return render(request,'user_center_info.html',context)
           
@login_required
def order(request):  #订单
	context = {
		
	}
	return render(request, 'user_center_order.html', context)

#class SiteView(View):  #给类加登录验证装饰器,可以在url中添加login_required
# class SiteView(LoginRequiredView):
class SiteView(LoginRequiredViewMixin,View):
	
	def get(self,request):
		#获取收货地址
		addr_list=Address.objects.filter(user=request.user)#user:收货地址和user关联;request.user:是中间件内加的
		context = {
			'title':'收获地址',
			'addr_list':addr_list,
		}
		return render(request, 'user_center_site.html', context)
	
	def post(self,request): #接受用户请求数据
		dict=request.POST
		receiver=dict.get('receiver')
		province=dict.get('province')
		city = dict.get('city')
		district = dict.get('district')
		addr123=dict.get('addr')
		code = dict.get('code')
		phone = dict.get('phone')
		default = dict.get('default')
		
		#构造反馈信息
		context={
			'title':'保存收货地址',
			'err_msg':'',
		}
		
		#验证数据的完整性
		if not all([receiver,province,city,district,addr,code,phone]):
			context['err_msg']='数据填写不完整'
			return render(request,'user_center_site.html',context)
		
		#创建并保存地址对象
		addr=Address()
		#当前地址对应的用户
		addr.user=request.user
		
		addr.receiver=receiver
		addr.province_id = province
		addr.city_id = city
		addr.district_id = district
		addr.addr = addr123
		addr.code = code
		addr.phone_number = phone
		if default is not None:
			addr.isDefault = True
		
		addr.save()
		
		return redirect('/user/site')
	
def area(request): #area视图帮助查询省市区的信息
	#接受上级地区的编号
	pid=request.GET.get('pid')
	if pid is None:
		#查询省
		slist=AreaInfo.objects.filter(aParent_isnull=True)
	else:
		#如果pid是省编号,则查询市
		#如果pid是市编号,则查询县
		slist=AreaInfo.objects.filter(aParent_id=pid)
	
	# #查询地址信息
	# slist=AreaInfo.objects.filter(aParent__isnull=True) #省信息
	#构造需要的数据格式
	slist2=[]
	for s in slist:
		slist2.append({'id':s.id,'title':s.title})  #遍历出省的id和title添加到列表
	return JsonResponse({'list':slist2})