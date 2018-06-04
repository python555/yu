# coding:utf8
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer12, SignatureExpired

# Celery('任务文件路径',broker='redis://ip:端口/数据库')
'''
引入复制此配置信息
'''''
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "ttxx.settings"
# 放到Celery服务器上时添加的代码
import django
django.setup()



app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/5')

@app.task  # 被装饰的函数成为celery中的一个任务
def send_user_active(user):  # 传入user可以拿到user.id和user.email
	# 将帐号信息进行加密
	serializer = Serializer12(settings.SECRET_KEY, 60 * 60 * 2)  # 设置加密
	value = serializer.dumps({'id': user.id})  # dumps为加密,为bytes类型
	value = value.decode()  # 转成字符串,用于拼接地址
	
	# 向用户发送邮件
	# msg='<a href="htthp://127.0.0.1:8000/user/active/%d">点击激活</a>'%user_id
	msg = '<a href="htthp://127.0.0.1:8000/user/active/%s">点击激活</a>' % value
	send_mail('天天先鲜激活', '', settings.EMALL_FROM, [user.email], html_message=msg)  # 其他参数不写,会自动去setting中找数据
