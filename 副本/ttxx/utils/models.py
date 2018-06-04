# coding:utf8
from django.db import models
#创建模型类
class BaseModel(models.Model):
	#添加时间
	add_date=models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
	#最近修改/更新时间
	update_date=models.DateTimeField(auto_now=True,verbose_name='修改时间')
	#逻辑删除
	isDelete=models.BooleanField(default=False,verbose_name='逻辑删除')
	
	class Meta:
		abstract=True  #设置抽象,不设置就必须创建一张表,但这里不需要创建表