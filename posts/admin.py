from django.contrib import admin
from .models import Post, Gallery
from comments.models import Comment

# Register your models here.

class CommentTabAdmin(admin.TabularInline):
    model = Comment

class GalleryAdmin(admin.TabularInline):
    model = Gallery
    
class PostAdmin(admin.ModelAdmin):
    inlines = [GalleryAdmin, CommentTabAdmin]
    list_editable = ['user', 'title', 'visibility']
    list_display = ['thumbnail', 'user', 'title', 'visibility']
    prepopulated_fields = {"slug": ("title", )}
    
admin.site.register(Post, PostAdmin)