from django.db import models
from users.models import CustomUser
from main.models import Unit, Service, Sell
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class ChatRoom(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chat_rooms')
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='admin_chat_rooms', limit_choices_to={'is_staff': True})
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    subject = models.CharField(max_length=255, help_text='Chat subject or topic')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Chat Room'
        verbose_name_plural = 'Chat Rooms'
        ordering = ['-updated_at']
        unique_together = [['user', 'content_type', 'object_id']]
    
    def __str__(self):
        related_obj = f" - {self.content_object}" if self.content_object else ""
        return f"Chat: {self.user.email} with Admin{related_obj}"

class ChatMessage(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'
        indexes = [
            models.Index(fields=['chat_room', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.sender.email} in {self.chat_room}: {self.message[:50]}"
