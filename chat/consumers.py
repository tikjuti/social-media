from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import base64
import os
import json
from datetime import datetime
import cloudinary
import cloudinary.uploader
import cloudinary.api
from userauths.models import User, Profile
from .models import ChatMessage

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
    
    def get_extension_from_bytes_data(self, bypes_data: str):
        header = bypes_data.split(',')[0].split(';')[0]
        splashIndex = header.find('/')
        return header[splashIndex + 1:]

    def process_image(self, bytes_data):
        extension = self.get_extension_from_bytes_data(bypes_data=str(bytes_data))
        bytes_data = bytes_data.replace(f'data:image/{extension};base64,', '')
        image_data = base64.b64decode(bytes_data)
        
        # Tạo tên file duy nhất dựa trên thời gian hiện tại
        current_datetime_str = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        fileName = current_datetime_str + '.' + extension
        
        # Tạo file tạm thời để lưu ảnh
        temp_file_path = os.path.join('/tmp', fileName)
        with open(temp_file_path, 'wb') as file:
            file.write(image_data)
        
        # Tải ảnh lên Cloudinary
        response = cloudinary.uploader.upload(temp_file_path)
        
        # Xóa file tạm sau khi upload
        os.remove(temp_file_path)
        
        # Trả về URL của ảnh trên Cloudinary
        return response['secure_url']

    def process_file(self, file_name, file_data):
        extension = self.get_extension_from_bytes_data(bypes_data=str(file_data))
        file_data = file_data.replace(f'data:application/{extension};base64,', '')
        content = base64.b64decode(file_data)
        
        # Tạo file tạm thời để lưu dữ liệu file đã giải mã
        temp_file_path = os.path.join('/tmp', file_name)
        with open(temp_file_path, 'wb') as file:
            file.write(content)
        
        # Tải tệp lên Cloudinary
        response = cloudinary.uploader.upload(temp_file_path, resource_type='raw')
        
        # Xóa file tạm sau khi upload
        os.remove(temp_file_path)
        
        # Trả về URL của tệp trên Cloudinary
        return response['secure_url']
    
    def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        print("==================== message_type = ", message_type)
        message = data.get('message')
        sender_username = data.get('sender')
        image = data.get('image')
        imageName= ''
        file_data = data.get('file_doc')
        file_name = data.get('file_name')
        uid = data.get('UID')
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
                'uid': uid
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))