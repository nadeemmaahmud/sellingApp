from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q, Max
from django.contrib.contenttypes.models import ContentType
from .models import ChatMessage, ChatRoom
from .serializers import (
    ChatMessageSerializer, ChatMessageCreateSerializer,
    ChatRoomSerializer, ChatRoomCreateSerializer
)
from main.models import Unit, Service, Sell

class ChatRoomListView(generics.ListAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ChatRoom.objects.filter(admin=user, is_active=True).order_by('-updated_at')
        else:
            return ChatRoom.objects.filter(user=user, is_active=True).order_by('-updated_at')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class ChatRoomCreateView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        serializer = ChatRoomCreateSerializer(data=request.data)
        if serializer.is_valid():
            from users.models import CustomUser
            
            user_id = serializer.validated_data['user_id']
            subject = serializer.validated_data['subject']
            related_type = serializer.validated_data.get('related_type')
            related_id = serializer.validated_data.get('related_id')
            
            user = CustomUser.objects.get(id=user_id)
            
            content_type = None
            content_object = None
            
            if related_type and related_id:
                if related_type == 'unit':
                    content_type = ContentType.objects.get_for_model(Unit)
                    content_object = Unit.objects.get(id=related_id)
                elif related_type == 'service':
                    content_type = ContentType.objects.get_for_model(Service)
                    content_object = Service.objects.get(id=related_id)
                elif related_type == 'sell':
                    content_type = ContentType.objects.get_for_model(Sell)
                    content_object = Sell.objects.get(id=related_id)
            
            chat_room, created = ChatRoom.objects.get_or_create(
                user=user,
                content_type=content_type,
                object_id=related_id,
                defaults={
                    'admin': request.user,
                    'subject': subject,
                }
            )
            
            if not created:
                chat_room.admin = request.user
                chat_room.subject = subject
                chat_room.is_active = True
                chat_room.save()
            
            return Response({
                'message': 'Chat room created successfully' if created else 'Chat room already exists',
                'data': ChatRoomSerializer(chat_room, context={'request': request}).data
            }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatRoomDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            if request.user.is_staff:
                chat_room = ChatRoom.objects.get(pk=pk, admin=request.user)
            else:
                chat_room = ChatRoom.objects.get(pk=pk, user=request.user)
            
            serializer = ChatRoomSerializer(chat_room, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ChatRoom.DoesNotExist:
            return Response({'error': 'Chat room not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, pk):
        try:
            if request.user.is_staff:
                chat_room = ChatRoom.objects.get(pk=pk, admin=request.user)
            else:
                return Response({'error': 'Only admin can update chat rooms'}, status=status.HTTP_403_FORBIDDEN)
            
            is_active = request.data.get('is_active')
            if is_active is not None:
                chat_room.is_active = is_active
                chat_room.save()
            
            return Response({
                'message': 'Chat room updated successfully',
                'data': ChatRoomSerializer(chat_room, context={'request': request}).data
            }, status=status.HTTP_200_OK)
        except ChatRoom.DoesNotExist:
            return Response({'error': 'Chat room not found'}, status=status.HTTP_404_NOT_FOUND)

class ChatMessageListView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        chat_room_id = self.request.query_params.get('chat_room_id')
        
        if not chat_room_id:
            return ChatMessage.objects.none()
        
        user = self.request.user
        
        try:
            if user.is_staff:
                chat_room = ChatRoom.objects.get(id=chat_room_id, admin=user)
            else:
                chat_room = ChatRoom.objects.get(id=chat_room_id, user=user)
            
            return chat_room.messages.all().order_by('timestamp')
        except ChatRoom.DoesNotExist:
            return ChatMessage.objects.none()

class ChatMessageCreateView(generics.CreateAPIView):
    serializer_class = ChatMessageCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class MarkMessagesReadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        chat_room_id = request.data.get('chat_room_id')
        
        if not chat_room_id:
            return Response({
                'error': 'chat_room_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if user.is_staff:
                chat_room = ChatRoom.objects.get(id=chat_room_id, admin=user)
            else:
                chat_room = ChatRoom.objects.get(id=chat_room_id, user=user)
            
            messages = chat_room.messages.filter(is_read=False).exclude(sender=user)
            count = messages.update(is_read=True)
            
            return Response({
                'message': f'{count} messages marked as read'
            }, status=status.HTTP_200_OK)
        except ChatRoom.DoesNotExist:
            return Response({
                'error': 'Chat room not found'
            }, status=status.HTTP_404_NOT_FOUND)

class UnreadMessageCountView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        if user.is_staff:
            chat_rooms = ChatRoom.objects.filter(admin=user, is_active=True)
        else:
            chat_rooms = ChatRoom.objects.filter(user=user, is_active=True)
        
        unread_count = 0
        for chat_room in chat_rooms:
            unread_count += chat_room.messages.filter(is_read=False).exclude(sender=user).count()
        
        return Response({
            'unread_count': unread_count
        }, status=status.HTTP_200_OK)
