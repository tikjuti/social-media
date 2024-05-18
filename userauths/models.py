from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.html import mark_safe
from shortuuid.django_fields import ShortUUIDField
from cloudinary.models import CloudinaryField
import cloudinary.uploader

# Create your models here.

RELATIONSHIP = (
    ('single', 'Single'),
    ('married', 'Married'),
    ('inrelationship', 'In Relationship'),
)

GENDER = (
    ("female", "Female"),
    ("male", "Male"),
)

WHO_CAN_SEE_MY_FRIENDS  = (
    ('Everyone', 'Everyone'),
    ('Friends', 'Friends'),
    ('Only Me', 'Only Me'),
)

class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=50, choices=GENDER)
    
    otp = models.CharField(max_length=100, blank=True, null=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    def __str__(self):
        return str(self.username)
    
    
class Profile(models.Model):
    pid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cover_image = CloudinaryField('cover_image', blank=True, null=True, default="https://res.cloudinary.com/ddfsqd1ru/image/upload/v1715963028/kenh9ewa1adngh4yyeoc.jpg")
    image = CloudinaryField('image', blank=True, null=True, default="https://res.cloudinary.com/ddfsqd1ru/image/upload/v1715963029/jjalhv4zektgahhxj6yw.jpg")
    full_name = models.CharField(max_length=255)
    bio = models.CharField(max_length=100, blank=True, null=True)
    about_me = models.CharField(max_length=255, blank=True, null=True) 
    phone = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=50, choices=GENDER, null=True)
    relationship = models.CharField(max_length=50, choices=RELATIONSHIP, null=True)
    friends_visibility = models.CharField(max_length=50, choices=WHO_CAN_SEE_MY_FRIENDS, null=True, default='Everyone')
    country = models.CharField(max_length=255, blank=True, null=True)  
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    working_at = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.URLField(default='https://instagram.com/', blank=True, null=True)
    verified = models.BooleanField(default=False)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    following = models.ManyToManyField(User, related_name='following', blank=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    blocked = models.ManyToManyField(User, related_name='blocked', blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
        
    
    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        if self.full_name:
            return str(self.full_name)
        else:
            return str(self.user.username)
        
    def thumbnail(self):
        return mark_safe('<img src="%s" width="50" height="50" object-fit:"cover" style="border-radius: 30px;" />' % (self.image.url))


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        
        profile = Profile.objects.create(user=instance)
        
        if profile.image:
            cloudinary_response_image = cloudinary.uploader.upload(
                profile.image,
                folder='media/user_{0}'.format(profile.user.id)
            )
            profile.image = cloudinary_response_image['secure_url']

        if profile.cover_image:
            cloudinary_response_cover_image = cloudinary.uploader.upload(
                profile.cover_image,
                folder='media/user_{0}'.format(profile.user.id)
            )
            profile.cover_image = cloudinary_response_cover_image['secure_url']

        profile.save()

def save_user_profile(sender, instance, **kwargs):
	# instance.profile.save()
    old_profile = Profile.objects.get(user=instance)

    # Kiểm tra nếu có ảnh mới và ảnh cũ tồn tại
    if instance.profile.image and old_profile.image:
        # Xóa ảnh cũ
        old_image_public_id = old_profile.image.split('/')[-1].split('.')[0]
        cloudinary.uploader.destroy(old_profile.image)

    # Upload ảnh mới nếu có
    if instance.profile.image:
        cloudinary_response_image = cloudinary.uploader.upload(
            instance.profile.image,
            folder='media/user_{0}'.format(old_profile.user.id)
        )
        instance.profile.image = cloudinary_response_image['secure_url']

    # Lưu thông tin hồ sơ
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
    