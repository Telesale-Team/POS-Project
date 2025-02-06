from django.contrib import admin
from . models import *
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'category']
    search_fields = ['name', 'category__name']  # ค้นหาจากชื่อและประเภทสินค้า
    list_filter = ['category']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

admin.site.register(Product,ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Unit)