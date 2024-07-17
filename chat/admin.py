from django.contrib import admin
from .models import ChatMessage


# Register your models here.

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'reciever' ,'message', 'image_paths', 'file_paths', 'file_name','date', 'is_read']
    
admin.site.register(ChatMessage, ChatMessageAdmin)
