import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatMessage

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        
        if not self.user.is_authenticated:
            await self.close()
            return
        
        if self.user.is_staff:
            self.room_name = f"admin_{self.user.id}"
        else:
            admin_users = await self.get_admin_users()
            if not admin_users:
                await self.close()
                return
            self.admin_user = admin_users[0]
            self.room_name = f"user_{self.user.id}_admin_{self.admin_user.id}"
        
        self.room_group_name = f"chat_{self.room_name}"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        chat_history = await self.get_chat_history()
        await self.send(text_data=json.dumps({
            'type': 'chat_history',
            'messages': chat_history
        }))
    
    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get('message', '').strip()
            
            if not message:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'Message cannot be empty'
                }))
                return
            
            if self.user.is_staff:
                receiver_id = data.get('receiver_id')
                if not receiver_id:
                    await self.send(text_data=json.dumps({
                        'type': 'error',
                        'message': 'Receiver ID is required for admin'
                    }))
                    return
                receiver = await self.get_user_by_id(receiver_id)
                if not receiver:
                    await self.send(text_data=json.dumps({
                        'type': 'error',
                        'message': 'Receiver not found'
                    }))
                    return
            else:
                receiver = self.admin_user
            
            chat_message = await self.save_message(self.user, receiver, message)
            
            message_data = {
                'type': 'chat_message',
                'message': {
                    'id': chat_message.id,
                    'sender': {
                        'id': self.user.id,
                        'email': self.user.email,
                        'first_name': self.user.first_name,
                        'last_name': self.user.last_name,
                    },
                    'receiver': {
                        'id': receiver.id,
                        'email': receiver.email,
                        'first_name': receiver.first_name,
                        'last_name': receiver.last_name,
                    },
                    'message': message,
                    'timestamp': chat_message.timestamp.isoformat(),
                    'is_read': chat_message.is_read
                }
            }
            
            await self.channel_layer.group_send(
                self.room_group_name,
                message_data
            )
            
            if self.user.is_staff:
                user_room_group = f"chat_user_{receiver.id}_admin_{self.user.id}"
                await self.channel_layer.group_send(
                    user_room_group,
                    message_data
                )
            else:
                admin_room_group = f"chat_admin_{receiver.id}"
                await self.channel_layer.group_send(
                    admin_room_group,
                    message_data
                )
        
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': str(e)
            }))
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
    
    @database_sync_to_async
    def get_admin_users(self):
        return list(User.objects.filter(is_staff=True, is_active=True))
    
    @database_sync_to_async
    def get_user_by_id(self, user_id):
        try:
            return User.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist:
            return None
    
    @database_sync_to_async
    def save_message(self, sender, receiver, message):
        return ChatMessage.objects.create(
            sender=sender,
            receiver=receiver,
            message=message
        )
    
    @database_sync_to_async
    def get_chat_history(self):
        if self.user.is_staff:
            messages = ChatMessage.objects.filter(
                sender=self.user
            ) | ChatMessage.objects.filter(
                receiver=self.user
            )
        else:
            messages = ChatMessage.objects.filter(
                sender=self.user,
                receiver__is_staff=True
            ) | ChatMessage.objects.filter(
                sender__is_staff=True,
                receiver=self.user
            )
        
        messages = messages.order_by('timestamp')[:100]
        
        return [
            {
                'id': msg.id,
                'sender': {
                    'id': msg.sender.id,
                    'email': msg.sender.email,
                    'first_name': msg.sender.first_name,
                    'last_name': msg.sender.last_name,
                },
                'receiver': {
                    'id': msg.receiver.id,
                    'email': msg.receiver.email,
                    'first_name': msg.receiver.first_name,
                    'last_name': msg.receiver.last_name,
                },
                'message': msg.message,
                'timestamp': msg.timestamp.isoformat(),
                'is_read': msg.is_read
            }
            for msg in messages
        ]
