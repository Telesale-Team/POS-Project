from django.contrib import admin
from . models import *
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    
admin.site.register(Category,CategoryAdmin)