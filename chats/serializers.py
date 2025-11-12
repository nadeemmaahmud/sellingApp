from rest_framework import serializers
from .models import ChatMessage, ChatRoom
from users.serializers import CustomUserSerializer
from main.models import Unit, Service, Sell
from django.contrib.contenttypes.models import ContentType

class ChatRoomSerializer(serializers.ModelSerializer):
    user_details = CustomUserSerializer(source='user', read_only=True)
    admin_details = CustomUserSerializer(source='admin', read_only=True)
    related_type = serializers.SerializerMethodField()
    related_id = serializers.SerializerMethodField()
    related_info = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatRoom
        fields = ['id', 'user', 'admin', 'user_details', 'admin_details', 
                  'subject', 'related_type', 'related_id', 'related_info',
                  'is_active', 'created_at', 'updated_at', 'unread_count']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_related_type(self, obj):
        if obj.content_type:
            return obj.content_type.model
        return None
    
    def get_related_id(self, obj):
        return obj.object_id
    
    def get_related_info(self, obj):
        if obj.content_object:
            return str(obj.content_object)
        return None
    
    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0

class ChatRoomCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    subject = serializers.CharField(max_length=255, required=True)
    related_type = serializers.ChoiceField(choices=['unit', 'service', 'sell'], required=False, allow_null=True)
    related_id = serializers.IntegerField(required=False, allow_null=True)
    
    def validate(self, attrs):
        from users.models import CustomUser
        
        user_id = attrs.get('user_id')
        try:
            user = CustomUser.objects.get(id=user_id)
            if user.is_staff:
                raise serializers.ValidationError("Cannot create chat room with another admin user.")
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        
        related_type = attrs.get('related_type')
        related_id = attrs.get('related_id')
        
        if related_type and related_id:
            if related_type == 'unit':
                if not Unit.objects.filter(id=related_id, user=user).exists():
                    raise serializers.ValidationError("Unit not found or does not belong to this user.")
            elif related_type == 'service':
                if not Service.objects.filter(id=related_id, unit__user=user).exists():
                    raise serializers.ValidationError("Service not found or does not belong to this user.")
            elif related_type == 'sell':
                if not Sell.objects.filter(id=related_id, unit__user=user).exists():
                    raise serializers.ValidationError("Sale not found or does not belong to this user.")
        
        return attrs

class ChatMessageSerializer(serializers.ModelSerializer):
    sender_details = CustomUserSerializer(source='sender', read_only=True)
    chat_room_details = ChatRoomSerializer(source='chat_room', read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'chat_room', 'sender', 'sender_details', 'chat_room_details',
                  'message', 'timestamp', 'is_read']
        read_only_fields = ['id', 'timestamp', 'sender']

class ChatMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['chat_room', 'message']
    
    def validate_chat_room(self, value):
        request = self.context.get('request')
        if request and request.user:
            if request.user.is_staff:
                if value.admin != request.user:
                    raise serializers.ValidationError("You can only send messages to your own chat rooms.")
            else:
                if value.user != request.user:
                    raise serializers.ValidationError("You can only send messages to your own chat rooms.")
        return value
