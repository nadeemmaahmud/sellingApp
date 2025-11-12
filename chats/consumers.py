import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatMessage, ChatRoom

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        
        if not self.user.is_authenticated:
            await self.close()
            return
        
        self.chat_room_id = self.scope['url_route']['kwargs'].get('room_id')
        
        if not self.chat_room_id:
            await self.close()
            return
        
        chat_room = await self.get_chat_room(self.chat_room_id)
        
        if not chat_room:
            await self.close()
            return
        
        self.room_group_name = f"chat_room_{self.chat_room_id}"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        chat_history = await self.get_chat_history(self.chat_room_id)
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
            
            chat_message = await self.save_message(self.chat_room_id, self.user, message)
            
            if not chat_message:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'Failed to save message'
                }))
                return
            
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
                    'message': message,
                    'timestamp': chat_message.timestamp.isoformat(),
                    'is_read': chat_message.is_read
                }
            }
            
            await self.channel_layer.group_send(
                self.room_group_name,
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
    def get_chat_room(self, room_id):
        try:
            if self.user.is_staff:
                return ChatRoom.objects.get(id=room_id, admin=self.user, is_active=True)
            else:
                return ChatRoom.objects.get(id=room_id, user=self.user, is_active=True)
        except ChatRoom.DoesNotExist:
            return None
    
    @database_sync_to_async
    def save_message(self, room_id, sender, message):
        try:
            chat_room = ChatRoom.objects.get(id=room_id, is_active=True)
            
            if sender.is_staff and chat_room.admin != sender:
                return None
            elif not sender.is_staff and chat_room.user != sender:
                return None
            
            return ChatMessage.objects.create(
                chat_room=chat_room,
                sender=sender,
                message=message
            )
        except ChatRoom.DoesNotExist:
            return None
    
    @database_sync_to_async
    def get_chat_history(self, room_id):
        try:
            chat_room = ChatRoom.objects.get(id=room_id)
            messages = chat_room.messages.all().order_by('timestamp')[:100]
            
            return [
                {
                    'id': msg.id,
                    'sender': {
                        'id': msg.sender.id,
                        'email': msg.sender.email,
                        'first_name': msg.sender.first_name,
                        'last_name': msg.sender.last_name,
                    },
                    'message': msg.message,
                    'timestamp': msg.timestamp.isoformat(),
                    'is_read': msg.is_read
                }
                for msg in messages
            ]
        except ChatRoom.DoesNotExist:
            return []
