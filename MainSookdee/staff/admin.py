from django.contrib import admin
from staff.models import ProfileUser,Customer
# Register your models here.

class ProfileUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'address','phone']
    search_fields = ['user']
    list_filter = ['user']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'address','phone']
    search_fields = ['user']
    list_filter = ['user']

admin.site.register(ProfileUser,ProfileUserAdmin)
admin.site.register(Customer,CustomerAdmin)