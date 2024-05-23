from django.db import models
from shortuuid.django_fields import ShortUUIDField
from userauths.models import User 

# Create your models here.

FRIEND_REQUEST = (
    ('pending', 'Pending'),
    ('accept', 'Accept'),
    ('reject', 'Reject'),
)

class FriendRequest(models.Model):
    fid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='request_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='request_receiver')
    status = models.CharField(max_length=10, choices=FRIEND_REQUEST, default='pending')
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender}"
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Friend Request"
        
        
class Friend(models.Model):
    fid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='friend')
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}"
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Friend"