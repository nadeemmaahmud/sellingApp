from django.urls import path
from .views import (
    ChatRoomListView, ChatRoomCreateView, ChatRoomDetailView,
    ChatMessageListView, ChatMessageCreateView, 
    MarkMessagesReadView, UnreadMessageCountView
)

app_name = 'chats'

urlpatterns = [
    path('rooms/', ChatRoomListView.as_view(), name='room-list'),
    path('rooms/create/', ChatRoomCreateView.as_view(), name='room-create'),
    path('rooms/<int:pk>/', ChatRoomDetailView.as_view(), name='room-detail'),
    path('messages/', ChatMessageListView.as_view(), name='message-list'),
    path('messages/create/', ChatMessageCreateView.as_view(), name='message-create'),
    path('messages/mark-read/', MarkMessagesReadView.as_view(), name='mark-read'),
    path('messages/unread-count/', UnreadMessageCountView.as_view(), name='unread-count'),
]
