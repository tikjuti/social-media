
from django.urls import path
from . import views

app_name = "calls"

urlpatterns = [
    path('<username>/video/', views.videoCall, name='videoCall'),
    path('get_token/', views.getToken),
    
    path('<username>/video/create_member/', views.createMember),
    path('video/get_member/', views.getMember),
    path('video/delete_member/', views.deleteMember),
]
