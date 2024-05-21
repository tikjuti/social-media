from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Post
from django.utils.timesince import timesince
from django.utils.text import slugify
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

import shortuuid    

# Create your views here.
@login_required
def index(request):
    return render(request, 'core/index.html')

@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('post-caption')
        visibility = request.POST.get('visibility')
        image = request.FILES.get('post-thumbnail', None)

        print("Title ============", title)
        print("thumbnail ============", image)
        print("visibility ============", visibility)

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