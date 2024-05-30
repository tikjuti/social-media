
from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.add_friend, name="add-friend"),
    path("accept/", views.accept_friend_request, name="accept-friend-request"),
    path("unfriend/", views.unfriend, name="unfriend"),
    path("reject/", views.reject_friend_request, name="reject-friend-request"),
]
