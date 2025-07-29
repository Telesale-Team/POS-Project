from django.contrib import admin
from .models import Order, OrderItem,Log

class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'total_price','status','created_at']
    search_fields = ['customer',"created_at"]
    list_filter = ['customer','created_at']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product','order', 'quantity','price']
    search_fields = ['product','order']
    list_filter = ['order']

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Log)

