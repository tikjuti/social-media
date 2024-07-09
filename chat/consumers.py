import base64
import os

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

import json

from facebook import settings
from userauths.models import Profile, User
from chat.models import ChatMessage

from datetime import datetime
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    
    def get_extension_from_bytes_data(self,bypes_data : str):
        header  = bypes_data.split(',')[0].split(';')[0]
        splashIndex = header.find('/')

        return header[splashIndex+1:]

    def process_image(self,bytes_data):
        extension = self.get_extension_from_bytes_data(bypes_data=str(bytes_data))
        bytes_data = bytes_data.replace(f'data:image/{extension};base64,','')
        image_data = base64.b64decode(bytes_data)
        uploads_folder = os.path.join(settings.MEDIA_ROOT, 'uploads/images')   
        current_datetime_str = datetime.now().strftime('%Y-%m-%d-%H-%M-%S') 
        fileName = current_datetime_str +'.'+ extension
        if not os.path.exists(uploads_folder):
            os.makedirs(uploads_folder)
        file_path = os.path.join(uploads_folder, fileName)
        with open(file_path, 'wb') as file:
            file.write(image_data)
        return fileName

    
    def process_file(self,file_name,file_data):
        extension = self.get_extension_from_bytes_data(bypes_data=str(file_data))
        file_data = file_data.replace(f'data:application/{extension};base64,','')
        content = base64.b64decode(file_data)
        uploads_folder = os.path.join(settings.MEDIA_ROOT, 'uploads/files')   
        if not os.path.exists(uploads_folder):
            os.makedirs(uploads_folder)
        file_path = os.path.join(uploads_folder, file_name)
        with open(file_path, 'wb') as file:
            file.write(content)

        
    def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        print("==================== message_type = ", message_type)
        print("==================== data = ", data)
        message = data.get('message')
        sender_username = data.get('sender')
        image = data.get('image')
        imageName= ''
        file_data = data.get('file_doc')
        file_name = data.get('file_name')
        try:
            sender = User.objects.get(username=sender_username)
            profile = Profile.objects.get(user=sender)
            profile_image = profile.image.url
            if(len(image) >0):
                imageName =  self.process_image(image)
            if (len(file_name) > 0 and len(file_data) > 0):
                self.process_file(file_name,file_data)
                #print(file_data)
        except User.DoesNotExist:
            profile_image = ''

        reciever = User.objects.get(username=data['reciever'])
        chat_message = ChatMessage(
            sender=sender,
            reciever=reciever,
            message=message,
            image_paths = imageName,
            file_paths = file_name
        )
        chat_message.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_username,
                'profile_image': profile_image,
                'reciever': reciever.username,
                'image_paths' : imageName,
                'file_paths' : file_name,
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))