from rest_framework import serializers
from .models import ChatMessage
from users.serializers import CustomUserSerializer

class ChatMessageSerializer(serializers.ModelSerializer):
    sender_details = CustomUserSerializer(source='sender', read_only=True)
    receiver_details = CustomUserSerializer(source='receiver', read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'receiver', 'sender_details', 'receiver_details', 
                  'message', 'timestamp', 'is_read']
        read_only_fields = ['id', 'timestamp', 'sender']
    
    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.user:
            receiver = attrs.get('receiver')
            if not request.user.is_staff and not receiver.is_staff:
                raise serializers.ValidationError("Users can only chat with admin.")
        return attrs

class ChatMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['receiver', 'message']
    
    def validate_receiver(self, value):
        request = self.context.get('request')
        if request and request.user:
            if not request.user.is_staff and not value.is_staff:
                raise serializers.ValidationError("You can only send messages to admin.")
            if request.user == value:
                raise serializers.ValidationError("You cannot send messages to yourself.")
        return value
