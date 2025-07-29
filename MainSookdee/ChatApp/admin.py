from django.contrib import admin
from ChatApp.models import *
# Register your models here.
admin.site.register(Room)

class MessageAdmin(admin.ModelAdmin):
    list_display = ['room', 'sender', 'message']
admin.site.register(Message, MessageAdmin)