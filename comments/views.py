
from django.views.decorators.csrf import csrf_exempt
from posts.models import Post
from .models import Comment
from django.utils.timesince import timesince
from django.http import JsonResponse

from notifications.views import send_notification
noti_new_comment = "New Comment"

# Create your views here.

@csrf_exempt
def comment_on_post(request):
    id = request.GET['id']
    comment = request.GET['comment']
    post = Post.objects.get(id=id)
    comment_count = Comment.objects.filter(post=post).count()
    user = request.user
    
    new_comment = Comment.objects.create(
        post = post,
        comment = comment,
        user = user
    )
    
    if new_comment.user != post.user:
        send_notification(post.user, user, post, new_comment, noti_new_comment)
        
    data = {
        'bool': True,  
        'comment': new_comment.comment,
        'profile_image': new_comment.user.profile.image.url,
        'date': timesince(new_comment.date),
        'comment_id': new_comment.id,
        'post_id': new_comment.post.id,
        "comment_count":comment_count + int(1)
    }
    
    return JsonResponse({'data': data})

