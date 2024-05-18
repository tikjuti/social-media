from django.contrib import admin
from .models import Comment, ReplyComment

# Register your models here.
class ReplyCommentTabAdmin(admin.TabularInline):
    model = ReplyComment


class CommentAdmin(admin.ModelAdmin):
    inlines = [ReplyCommentTabAdmin]
    list_display = ['user', 'post', 'comment', 'active']
    
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'active']

admin.site.register(Comment, CommentAdmin)
admin.site.register(ReplyComment, ReplyAdmin)