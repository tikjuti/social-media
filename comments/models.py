from django.db import models
from userauths.models import User
from shortuuid.django_fields import ShortUUIDField
import shortuuid

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    cid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username
    
    class Meta: 
        ordering = ['-date']
        verbose_name_plural = 'Comment'
    
    def comment_replies(self):
        comment_replies = ReplyComment.objects.filter(comment=self)
        return comment_replies
    
    
        
class ReplyComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    cid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Reply Comment'
        
    