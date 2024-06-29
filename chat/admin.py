from django.contrib import admin
from .models import ChatMessage

# Register your models here.

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'reciever' ,'message','date', 'is_read']
    
admin.site.register(ChatMessage, ChatMessageAdmin)