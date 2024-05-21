from django.contrib import admin
from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("", views.index, name="feed"),
    
    
    path("create-post/", views.create_post, name="create-post"),
]
