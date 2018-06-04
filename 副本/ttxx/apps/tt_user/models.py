from django.db import models

# Create your models here.
from utils.models import BaseModel
from django.contrib.auth.models import AbstractUser #自带的管理系统

class User(BaseModel,AbstractUser):
	class Meta:
		db_table='tt_user'  #将来生成的类,生成的表的名字为tt_user
class AreaInfo(models.Model):  #区域,不需要维护不需要添加时间更新时间,所以不用继承其他
	title=models.CharField(max_length=20)
	aParent=models.ForeignKey('self',null=True,blank=True) #self为关联意思
	class Meta:
		db_table='tt_area'  #表起名
		
class Address(BaseModel):  #收获地址
	receiver=models.CharField(max_length=10)  #收件人
	province=models.ForeignKey('AreaInfo',related_name='province')  #related_name为自定义关联,不指定会因重名报错
	city=models.ForeignKey('AreaInfo',related_name='city') #related_name为自定义关联,不指定会因重名报错
	district=models.ForeignKey('AreaInfo',related_name='district') #related_name为自定义关联,不指定会因重名报错
	addr=models.CharField(max_length=20)  #地址
	code=models.CharField(max_length=6) #邮编
	phone_number=models.CharField(max_length=11) #电话
	isDefault = models.BooleanField(default=0) #是否默认
	user=models.ForeignKey('User')#关联省和用户关系
	
	class Meta:
		db_table='df_address' #起名