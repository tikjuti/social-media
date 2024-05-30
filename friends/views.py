from django.views.decorators.csrf import csrf_exempt
from userauths.models import User
from .models import Friend, FriendRequest
from django.utils.timesince import timesince
from django.http import JsonResponse

from notifications.views import send_notification

noti_friend_request = "Friend Request"
noti_friend_request_accepted = "Friend Request Accepted"
# Create your views here.

@csrf_exempt
def add_friend(request):
    sender = request.user
    receiver_id = request.GET['id']
    
    bool = False
    
    if sender.id == int(receiver_id):
        return JsonResponse({'data': 'You cannot send friend request to yourself'})
    
    receiver = User.objects.get(id=receiver_id)
    
    try:
        friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver)
        if friend_request:
            friend_request.delete()
        bool = False
        return JsonResponse({'error': 'Cancelled', 'bool':bool})
    
    except FriendRequest.DoesNotExist:
        friend_request = FriendRequest(sender=sender, receiver=receiver)
        friend_request.save()
        bool = True
        
        send_notification(receiver, sender, None, None, noti_friend_request)
        
        return JsonResponse({'success': 'Sent',  'bool':bool})
    
    
@csrf_exempt
def accept_friend_request(request):
    id = request.GET['id']
    
    receiver = request.user
    sender = User.objects.get(id=id)
    
    friend_request = FriendRequest.objects.filter(sender=sender, receiver=receiver).first()
    
    receiver.profile.friends.add(sender)
    sender.profile.friends.add(receiver)
    
    Friend.objects.create(user=receiver, friend=sender)
    
    friend_request.delete()
    
    send_notification(sender, receiver, None, None, noti_friend_request_accepted)
    
    data = {
        "message":"Accepted",
        "bool":True,
    }
    
    return JsonResponse({'data': data})

@csrf_exempt
def unfriend(request):
    friend_id  = request.GET['id']
    sender = request.user
    bool = False
    
    if sender.id == int(friend_id):
        return JsonResponse({'error': 'You cannot unfriend yourself, wait a minute how did you even send yourself a friend request?.'})
    
    my_friend = User.objects.get(id=friend_id)
    
    if my_friend in sender.profile.friends.all():
        sender.profile.friends.remove(my_friend)
        my_friend.profile.friends.remove(sender)
        Friend.objects.filter(user=sender, friend=my_friend).delete()
        bool = True
        return JsonResponse({'success': 'Unfriend Successfull',  'bool':bool})
    
    
@csrf_exempt
def reject_friend_request(request):
    id = request.GET['id']
    
    receiver = request.user
    sender = User.objects.get(id=id)
    
    friend_request = FriendRequest.objects.filter(sender=sender, receiver=receiver).first()
    friend_request.delete()
    
    data = {
        'message': 'Rejected',
        'bool': True
    }
    
    return JsonResponse({'data': data})


def block_user(request):
    id = request.GET['id']
    user = request.user
    friend = User.objects.get(id=id)
    
    if user.id == friend.id:
        return JsonResponse({'error': 'You cannot block yourself'})

    if friend in user.profile.friends.all():
        user.profile.blocked.add(friend)
        user.profile.friends.remove(friend)
        friend.profile.friends.remove(user)
        Friend.objects.filter(user=user, friend=friend).delete()
        
    else:
        return JsonResponse({'error': 'You are not friends with this user'})

    return JsonResponse({'success': 'Blocked'})
    
    