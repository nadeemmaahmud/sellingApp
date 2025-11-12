from django.contrib import admin
from .models import ChatMessage, ChatRoom

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'admin', 'subject', 'content_type', 'object_id', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'content_type']
    search_fields = ['user__email', 'admin__email', 'subject']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat_room', 'sender', 'message_preview', 'timestamp', 'is_read']
    list_filter = ['is_read', 'timestamp']
    search_fields = ['sender__email', 'message', 'chat_room__subject']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'
