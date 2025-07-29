from django.contrib import admin
from . models import *
from django.http import JsonResponse
from django.urls import path
from django.utils.html import format_html
# Register your models here.

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone_number', 'email', 'created_at')
    search_fields = ('name', 'email')

class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'created_at')
    search_fields = ('name',)

class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'movement_type', 'quantity', 'movement_date', 'reference_number', 'created_by')
    list_filter = ('movement_type', 'warehouse', 'created_by')
    search_fields = ('product__name', 'reference_number')



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'check_data','date_stamp']
    search_fields = ['name']
    list_filter = ['name']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name','unit', 'price','cost','stock_quantity','category']
    search_fields = ['name', 'category__name']  # ค้นหาจากชื่อและประเภทสินค้า
    list_filter = ['category']

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product_id','product','image','is_primary']
    ist_editable = ['order']
    search_fields = ['product']
    list_filter = ['product']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        return "-"
    image_preview.short_description = "Preview"


admin.site.register(StockInventory,StockMovementAdmin)
admin.site.register(Warehouse,WarehouseAdmin)
admin.site.register(Supplier,SupplierAdmin)
admin.site.register(ProductImage,ProductImageAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Unit,UnitAdmin)
