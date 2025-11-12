from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import ChatMessage
from .serializers import ChatMessageSerializer, ChatMessageCreateSerializer

class ChatMessageListView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            user_id = self.request.query_params.get('user_id')
            if user_id:
                return ChatMessage.objects.filter(
                    Q(sender=user, receiver_id=user_id) | 
                    Q(sender_id=user_id, receiver=user)
                ).order_by('timestamp')
            return ChatMessage.objects.filter(
                Q(sender=user) | Q(receiver=user)
            ).order_by('timestamp')
        else:
            return ChatMessage.objects.filter(
                Q(sender=user, receiver__is_staff=True) | 
                Q(sender__is_staff=True, receiver=user)
            ).order_by('timestamp')

class ChatMessageCreateView(generics.CreateAPIView):
    serializer_class = ChatMessageCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class MarkMessagesReadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        sender_id = request.data.get('sender_id')
        
        if not sender_id:
            return Response({
                'error': 'sender_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        messages = ChatMessage.objects.filter(
            sender_id=sender_id,
            receiver=user,
            is_read=False
        )
        
        count = messages.update(is_read=True)
        
        return Response({
            'message': f'{count} messages marked as read'
        }, status=status.HTTP_200_OK)

class UnreadMessageCountView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        if user.is_staff:
            unread_count = ChatMessage.objects.filter(
                receiver=user,
                is_read=False,
                sender__is_staff=False
            ).count()
        else:
            unread_count = ChatMessage.objects.filter(
                receiver=user,
                is_read=False,
                sender__is_staff=True
            ).count()
        
        return Response({
            'unread_count': unread_count
        }, status=status.HTTP_200_OK)

class ChatUsersListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        if not user.is_staff:
            return Response({
                'error': 'Only admin can view chat users list'
            }, status=status.HTTP_403_FORBIDDEN)
        
        from users.models import CustomUser
        from django.db.models import Max, Count
        
        users_with_messages = CustomUser.objects.filter(
            Q(sent_messages__receiver=user) | Q(received_messages__sender=user)
        ).distinct().annotate(
            last_message_time=Max('sent_messages__timestamp'),
            unread_count=Count('sent_messages', filter=Q(sent_messages__receiver=user, sent_messages__is_read=False))
        ).values(
            'id', 'email', 'first_name', 'last_name', 'last_message_time', 'unread_count'
        ).order_by('-last_message_time')
        
        return Response(list(users_with_messages), status=status.HTTP_200_OK)
