from django.urls import path
from .views import (
    ChatMessageListView, ChatMessageCreateView, 
    MarkMessagesReadView, UnreadMessageCountView,
    ChatUsersListView
)

app_name = 'chats'

urlpatterns = [
    path('messages/', ChatMessageListView.as_view(), name='message-list'),
    path('messages/create/', ChatMessageCreateView.as_view(), name='message-create'),
    path('messages/mark-read/', MarkMessagesReadView.as_view(), name='mark-read'),
    path('messages/unread-count/', UnreadMessageCountView.as_view(), name='unread-count'),
    path('users/', ChatUsersListView.as_view(), name='chat-users'),
]
