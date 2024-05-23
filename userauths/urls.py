from django.urls import path 
from userauths import views 
from django.contrib.auth import views as auth_views

app_name = "userauths"

urlpatterns = [
    path("register/", views.RegisterView, name="register"),
    path("login/", views.LoginView, name="login"),
    path("logout/", views.LogoutView, name="logout"),
    
    path("my-profile/", views.my_profile, name="my-profile"),
    path("profile/<username>/", views.friend_profile, name="profile"),
    path("profile-update/", views.profile_update, name="profile-update"),
    path("search/", views.search_users, name="search_users"),
    
    # Change password
    path("change-password/", auth_views.PasswordChangeView.as_view(template_name='userauths/password-reset/change-password.html',
                                               success_url = '/user/password-reset-complete/'), name="change_password"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='userauths/password-reset/password_reset_complete.html'), 
                                                    name='password_reset_complete'),
]