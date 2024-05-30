from django.db import models
from userauths.models import User
from cloudinary.models import CloudinaryField
import cloudinary.uploader
from shortuuid.django_fields import ShortUUIDField
import shortuuid
from django.utils.text import slugify
from django.utils.html import mark_safe
from comments.models import Comment

# Create your models here.

VISIBILITY = (
    ('Everyone', 'Everyone'),
    ('Only Me', 'Only Me'),
)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    image = CloudinaryField('image', folder="media", blank=True, null=True)
    video = CloudinaryField('video', folder="media", blank=True, null=True) 
    visibility = models.CharField(max_length=50, choices=VISIBILITY, default='public')
    pid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    like = models.ManyToManyField(User, related_name='likes', blank=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    views = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Post'
    
    def save(self, *args, **kwargs):
        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title) + "-" + str(uniqueid.lower())    
            
        super(Post, self).save(*args, **kwargs) 
        
    def thumbnail(self):
        return mark_safe('<img src="%s" width="50" height="50" object-fit:"cover" style="border-radius: 5px;" />' % (self.image.url))
    
    def gallery(self):
        return Gallery.objects.filter(post=self)
    
    def title_len_count(self):
        return len(self.title)
    
    def gallery_count(self):
        return Gallery.objects.filter(post=self).count()
    
    def post_comments(self):
        return Comment.objects.filter(post=self, active=True)
    
    def post_comments_count(self):
        return Comment.objects.filter(post=self, active=True).count()
        
        
class Gallery(models.Model):
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    image = CloudinaryField('image', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.post)
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Gallery'
        
    def save(self, *args, **kwargs):
        if self.image:
            cloudinary.uploader.upload(
                self.image,
                folder='media/gallery'
            )
        super(Gallery, self).save(*args, **kwargs)
    
    def thumbnail(self):
        return mark_safe('<img src="%s" width="50" height="50" object-fit:"cover" style="border-radius: 30px;" />' % (self.image.url))
    
        