from django.contrib import admin

# Register your models here.
from .models import GoodsCategory,Goods,GoodsSKU,GoodsImage,IndexCategoryGoodsBanner,IndexGoodsBanner,IndexPromotionBanner

#models的每个类注册一遍
admin.site.register(GoodsCategory)
admin.site.register(Goods)
admin.site.register(GoodsSKU)
admin.site.register(GoodsImage)
admin.site.register(IndexCategoryGoodsBanner)
admin.site.register(IndexGoodsBanner)
admin.site.register(IndexPromotionBanner)
