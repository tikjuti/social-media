from django.urls import path 
from userauths import views 

app_name = "userauths"

urlpatterns = [
    path("register/", views.RegisterView, name="register"),
    path("login/", views.LoginView, name="login"),
    path("logout/", views.LogoutView, name="logout"),
    
    path("profile-update/", views.profile_update, name="profile-update"),
    path("my-profile/", views.my_profile, name="my-profile"),
    path("search/", views.search_users, name="search_users"),
]