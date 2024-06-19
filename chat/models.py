from django.db import models
from django.utils.html import mark_safe
from userauths.models import User

# Create your models here.

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
    reciever = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reciever")
    message = models.CharField(max_length=10000000)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    image_paths = models.CharField(max_length=10000000000,default='')
    file_paths = models.CharField(max_length=10000000000,default='')
    
    def __str__(self):
        return self.sender.username
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Personal Chat"
