from django.contrib import admin
from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("", views.index, name="feed"),
    
    
    path("create-post/", views.create_post, name="create-post"),
    path("delete-post/", views.delete_post, name="delete-post"),
    path("get-post/", views.get_post, name="get-post"),
    path("edit-post/", views.edit_post, name="edit-post"),
    
    path("post/<slug:slug>/", views.post_detail, name="post-detail"),
    path('load_more_posts/', views.load_more_posts, name='load_more_posts'),
]
