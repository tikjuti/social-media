from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Subquery
from django.db.models import Q, Count, Sum, F, FloatField
from .models import ChatMessage
from userauths.models import User

# Create your views here.

@login_required
def inbox_detail(request, username):
    user_id = request.user
    
    message_list = ChatMessage.objects.filter(
        id__in =  Subquery(
            User.objects.filter(
                Q(sender__reciever=user_id) |
                Q(reciever__sender=user_id)
            ).distinct().annotate(
                last_msg=Subquery(
                    ChatMessage.objects.filter(
                        Q(sender=OuterRef('id'),reciever=user_id) |
                        Q(reciever=OuterRef('id'),sender=user_id)
                    ).order_by('-id')[:1].values_list('id',flat=True) 
                )
            ).values_list('last_msg', flat=True).order_by("-id")
        )
    ).order_by("-id")   
    
    sender = request.user
    receiver = User.objects.get(username=username)
    receiver_details = User.objects.get(username=username)
    
    messages_detail = ChatMessage.objects.filter(
        Q(sender=sender, reciever=receiver) | Q(sender=receiver, reciever=sender)
    ).order_by("date")
    
    messages_detail.update(is_read=True)
    if messages_detail:
        r = messages_detail.first()
        reciever = User.objects.get(username=r.reciever)
    else:
        reciever = User.objects.get(username=username)

    context = {
        'message_detail': messages_detail,
        "reciever":reciever,
        "sender":sender,
        "receiver_details":receiver_details,
        "message_list":message_list,
    }
    return render(request, 'chat/inbox_detail.html', context)

    