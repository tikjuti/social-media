from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("post/", views.comment_on_post, name="comment-post"),
    path("like/", views.like_comment, name="like-comment"),
    path("reply/", views.reply_comment, name="reply-comment"),
    path("delete/", views.delete_comment, name="delete-comment"),
]
