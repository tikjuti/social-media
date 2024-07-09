from django.shortcuts import render
import random
import time
import json
from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import RoomVideoCall


# Create your views here.
def videoCall(request, username):
    return render(request, 'call/create_room_call.html')

def getToken(request):
    appId = "0eb423f7127d4e1bbdaa5b4bbb5994b9"
    appCertificate = "b8374550470f4182b4a2cfd159fe2be6"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)

@csrf_exempt
def createMember(request, username):
    data = json.loads(request.body)
    member, created = RoomVideoCall.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    try:
        member = RoomVideoCall.objects.get(
            uid=uid,
            room_name=room_name,
        )
        name = member.name
        return JsonResponse({'name': member.name}, safe=False)
    except RoomVideoCall.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)
    
@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    
    try:
        member = RoomVideoCall.objects.get(
            name=data['name'],
            uid=data['UID'],
            room_name=data['room_name']
        )
        member.delete()
        return JsonResponse('Member deleted', safe=False)
    except RoomVideoCall.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)
