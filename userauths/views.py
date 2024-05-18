from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from userauths.forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm

from userauths.models import User, Profile

# Create your views here.

def RegisterView(request, *args, **kwargs):
    if request.user.is_authenticated:
        messages.warning(request, f"Người dùng {request.user.username} đã đăng nhập ")
        return redirect('posts:feed')
    
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        full_name = form.cleaned_data.get('full_name')
        phone = form.cleaned_data.get('phone')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        
        user = authenticate(email=email, password=password)
        login(request, user)
        
        messages.success(request, f"Xin chào {request.user.username}, tài khoản của bạn đã đươc tạo thành công.")
        
        profile = Profile.objects.get(user=request.user)
        profile.full_name = full_name
        profile.phone = phone
        profile.save()
        
        return redirect('posts:feed')
    
    context = {'form': form}
    
    return render(request, 'userauths/register.html', context)