
from django.views.decorators.csrf import csrf_exempt
from posts.models import Post
from .models import Comment, ReplyComment
from django.utils.timesince import timesince
from django.http import JsonResponse

from notifications.views import send_notification

noti_new_comment = "New Comment"
noti_comment_liked = "Comment Liked"
noti_comment_replied = "Comment Replied"

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


@csrf_exempt
def like_comment(request):
    id = request.GET['id']
    comment = Comment.objects.get(id=id)
    user = request.user
    bool = False
    
    if user in comment.likes.all():
        comment.likes.remove(user)
        bool = False
    else:
        comment.likes.add(user)
        bool = True
        
        if comment.user != user:
            send_notification(comment.user, user, comment.post, comment, noti_comment_liked)
    
    data = {
        'bool': bool,
        'likes': comment.likes.count()
    }
    
    return JsonResponse({'data': data})


@csrf_exempt
def reply_comment(request):
    id = request.GET['id']
    reply = request.GET['reply']
    
    comment =Comment.objects.get(id=id)
    user = request.user
    
    new_reply = ReplyComment.objects.create(
        comment = comment,
        reply = reply,
        user = user
    )
    
    if comment.user != user:
        send_notification(comment.user, user, comment.post, comment, noti_comment_replied)

    data = {
        'bool': True,
        'reply': new_reply.reply,
        'profile_image': new_reply.user.profile.image.url,
        'date': timesince(new_reply.date),
        'reply_id': new_reply.id,
        'post_id': new_reply.comment.post.id
    }
    
    return JsonResponse({'data': data})


@csrf_exempt
def delete_comment(request):
    id = request.GET['id']
    
    comment = Comment.objects.get(id=id, user=request.user)
    comment.delete()
    
    data = {
        'bool': True,
    }
    
    return JsonResponse({'data': data})