from django.shortcuts import render

# Create your views here.
from tt_goods.models import GoodsCategory,IndexGoodsBanner,IndexPromotionBanner,IndexCategoryGoodsBanner

#FDFS获取图片
def test(request):
	category=GoodsCategory.objects.get(pk=1)
	context={
		'category':category,
	}
	return render(request,'fdfs_test.html',context)


def index(request):
	#查询分类信息
	category_list=GoodsCategory.objects.all()  #==模型类.管理器.all()
	
	#查询首页轮波图片
	banner_list=IndexGoodsBanner.objects.all().order_by('index') #根据index字段排序,自定义排序字段
	
	#查询首页广告位数据
	adv_list=IndexPromotionBanner.objects.all().order_by('index')
	
	#查询分类的推荐商品信息
	for category in category_list:
		#查询当前分类的推荐文本商品
		title_list=IndexCategoryGoodsBanner.objects.filter(category=category,display_type=0).order_by('index')[0:3]
		category.title_list=title_list
		#查询当前分类的推荐图片商品
		image_list = IndexCategoryGoodsBanner.objects.filter(category=category, display_type=1).order_by('index')[0:4]
		category.image_list = image_list
	context={
		'title':'首页',
		'category_list':category_list,
		'banner_list':banner_list,
		'adv_list':adv_list,
	}
	for c in category_list:
		print(c.title_list,c.image_list)
	return render(request,'index.html',context)