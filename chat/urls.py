
from django.urls import path
from . import views

app_name = "chats"

urlpatterns = [
    path("<username>/", views.inbox_detail, name="inbox_detail"),
]
