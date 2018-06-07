# #coding:utf8
#
# #通过这个类可以向fastDFS服务器上传文件
# from fdfs_client.client import Fdfs_client
#
# #根据配置文件创建客户端对象
# #在配置文件中指定类tracker服务器
# #tracker服务器负责管理跟踪,storage服务器负责保存上传数据
# client=Fdfs_client('/etc/fdfs/client.conf')
#
# #上传文件
# result=client.upload_by_file('01.jpg') #需要用桥接,并固定ip
# print(result) #为字典
#
# #{'Remote file_id': 'group1/M00/00/00/wKhfjFsYERWATNK7AAAuVCnSMv8252.bmp', 'Group name': 'group1', 'Storage IP': '192.168.95.140', 'Status': 'Upload successed.', 'Local file name': '2.bmp', 'Uploaded size': '11.00KB'}
#
#
# #访问文件需要nginx,每次停机数据都会消失,每次上传数据文件名都会变化
# #浏览器输入即可访问:localhost:8888/group1/M00/00/00/wKhfjFsYERWATNK7AAAuVCnSMv8252.bmp
