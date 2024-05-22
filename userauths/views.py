from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from userauths.forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm

from userauths.models import User, Profile
from posts.models import Post

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


def LoginView(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(email=email, password=password)
            if user is not None :
                login(request, user)
                # messages.success(request, "Đăng nhập thành công")
                return redirect('posts:feed')
            else :
                messages.error(request, "Email hoặc mật khẩu không đúng")
        except:
            messages.error(request, "Người dùng không tồn tại")
    return HttpResponseRedirect("/")

def LogoutView(request):
    logout(request)
    messages.success(request, 'Đăng xuất thành công')
    return redirect("userauths:register")


@login_required
def my_profile(request):
    profile = request.user.profile
    posts = Post.objects.filter(user=request.user, active = True)
    # groups = Group.objects.filter(active=True, user=request.user)
    
    context = {
        'posts': posts,
        'profile': profile,
        # 'groups': groups,
    }
    
    return render(request, 'userauths/my-profile.html', context)


@login_required
def profile_update(request):
    if  request.method == "POST":
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile) 
        # print(p_form)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        print(request.POST)

        # Lấy dữ liệu từ request.POST và request.FILES
        # image = request.FILES.get('image')
        # cover_image = request.FILES.get('cover_image')
        # full_name = request.POST.get('full_name')
        # bio = request.POST.get('bio')
        # about_me = request.POST.get('about_me')
        # gender = request.POST.get('gender')
        # relationship = request.POST.get('relationship')
        # phone = request.POST.get('phone')
        # friends_visibility = request.POST.get('friends_visibility')
        # country = request.POST.get('country')
        # city = request.POST.get('city')
        # state = request.POST.get('state')
        # address = request.POST.get('address')
        # working_at = request.POST.get('working_at')
        # instagram = request.POST.get('instagram')

        # Tạo một bản ghi mới trong bảng Post
        # Profile.objects.create(
        #     image=image,
        #     cover_image=cover_image,
        #     full_name=full_name,
        #     bio=bio,
        #     about_me=about_me,
        #     gender=gender,
        #     relationship=relationship,
        #     phone=phone,
        #     friends_visibility=friends_visibility,
        #     country=country,
        #     city=city,
        #     state=state,
        #     address=address,
        #     working_at=working_at,
        #     instagram=instagram
        # )

        
        p_form.save()
        u_form.save()
        print("Profile updated")
        messages.success(request, 'Hồ sơ đã cập nhật thành công')
        return redirect('userauths:profile-update')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)
    
    context = {
        'p_form': p_form,
        'u_form': u_form,
    }
    
    return render(request, 'userauths/profile-update.html', context)
        