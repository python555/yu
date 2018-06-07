# coding:utf8
from django.conf import settings
from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client

#自定义的存储类,必须继承自Storage,才能被django所识别,在settings中的配置才有效
class FdfsStorage(Storage):
	
	def __init__(self):
		self.client=settings.FDFS_CLIENT
		self.server=settings.FDFS_SERVER
	
	#读取文件不需要用这个对象,因为文件存储在fdfs中的nginx读取的
	def open(self, name, mode='rb'):
		pass
		pass
	#django调用保存类进行文件保存时,这个方法会被调用
	#content就是要保存的文件数据
	def save(self, name, content, max_length=None):  #save为Storage的一个方法
		
		#读取文件数据
		buffer12=content.read()
		
		# 通过这个类可以向fastDFS服务器上传文件
		# from fdfs_client.client import Fdfs_client
		
		# 根据配置文件创建客户端对象
		# 在配置文件中指定类tracker服务器
		# tracker服务器负责管理跟踪,storage服务器负责保存上传数据
		# client = Fdfs_client('/etc/fdfs/client.conf')  #有个弊端,文件拷贝后此路径文件不存在,最好手动拷贝到自己的文件夹下
		client = Fdfs_client(self.client)
		
		try:
			# 上传文件
			# result = client.upload_by_file('2.bmp')  # 需要用桥接,并固定ip
			result = client.upload_by_buffer(buffer12)  # 需要用桥接,并固定ip
			print(result)  # result为字典

		except:
			raise
		
		if result.get('Status')=='Upload successed.':
			print(result.get('Status'))  # result为字典
			return result.get('Remote file_id')
		else:
			raise Exception('文件上传失败')
		
	
	# {'Remote file_id': 'group1/M00/00/00/wKhfjFsYERWATNK7AAAuVCnSMv8252.bmp', 'Group name': 'group1', 'Storage IP': '192.168.95.140', 'Status': 'Upload successed.', 'Local file name': '2.bmp', 'Uploaded size': '11.00KB'}
	
	
	# 访问文件需要nginx,每次停机数据都会消失,每次上传数据文件名都会变化
	# 浏览器输入即可访问:localhost:8888/group1/M00/00/00/wKhfjFsYERWATNK7AAAuVCnSMv8252.bmp
		
	#GoodScategory通过category.image.url来获取图片文件的地址,这个url属性返回的是存储对象的Uel方法的值
	#在表中保存的数据为group1/M00/00/00/wKhfjFsYERWATNK7AAAuVCnSMv8252.bmp
	#实际获取图片的地址是:'HTTP://localhost:8888/'+name==
	def url(self, name):
		# return 'http://localhost:8888/'+name
		return self.server + name

