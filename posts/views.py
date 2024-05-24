from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Post
from django.utils.timesince import timesince
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

import shortuuid    
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
@login_required
def index(request):
    posts = Post.objects.filter(active=True, visibility="Everyone")
    
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    context = {
        "posts": posts
    }
    return render(request, 'core/index.html', context)

@login_required
def post_detail(request, slug):
    post = Post.objects.get(active=True, visibility="Everyone", slug=slug)
    context = {
        "p":post
    }
    return render(request, "post/post-detail.html", context)

@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('post-caption')
        visibility = request.POST.get('visibility')
        image = request.FILES.get('post-thumbnail', None)

        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]

        if title or image:
            post = Post(title=title, visibility=visibility, user=request.user, slug=slugify(title) + "-" + str(uniqueid.lower()))
            if image:
                post.image = image
            post.save()

            
            return JsonResponse({'post': {
                'title': post.title,
                'image_url': post.image.url if post.image else None,
                "full_name":post.user.profile.full_name,
                "profile_image":post.user.profile.image.url,
                "date":timesince(post.date),
                "id":post.id,
            }})
        else:
            return JsonResponse({'error': 'Invalid post data'})

    return JsonResponse({"data":"Sent"})

def load_more_posts(request):
    all_posts = Post.objects.filter(active=True, visibility="Everyone").order_by('-date')
    
    paginator = Paginator(all_posts, 3)
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)
    
    posts_data = []
    for post in page_obj:
        post_data = {
            'title': post.title,
            'profile_image': post.user.profile.image.url,
            'full_name': post.user.profile.full_name,
            'image_url': post.image.url if post.image else None,
            'video': post.video.url if post.video else None,
            'id': post.id,
            'likes': post.like.count(),
            'slug': post.slug,
            'views': post.views,
            'date': timesince(post.date),
        }
        
        posts_data.append(post_data)
    return JsonResponse({'posts': posts_data})

@csrf_exempt
def delete_post(request):
    id = request.GET['id']
    post = Post.objects.get(id=id)
    post.delete()

    data = {
        "bool":True,
    }
    return JsonResponse({"data":data})


def get_post(request):
    try:
        post_id = request.GET['id']
        post = Post.objects.get(id=post_id)

        posts = {
            "title": post.title,
            "image": post.image.url,
            "visibility": post.visibility
        }
        return JsonResponse(posts)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)


@csrf_exempt
def edit_post(request):
    try:
        if request.method == 'POST':
            post_id = request.POST.get('post-id')
            title = request.POST.get('post-caption')
            visibility = request.POST.get('visibility')
            post = Post.objects.get(id=post_id)

            image = request.FILES.get('post-thumbnail') if 'post-thumbnail' in request.FILES else request.POST.get('url-image')
            print("image = ", image)
            if image:
                if 'post-thumbnail' in request.POST and '/media/' in image:
                    image = image.replace('/media/', '') 
                post.image = image
                print(post.image)


            post.title = title
            post.visibility = visibility
            post.save()

            updated_post = {
                "title": post.title,
                "image": post.image.url,
                "visibility": post.visibility
            }
            return JsonResponse(updated_post)
        else:
            return HttpResponse("Invalid request method")
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)