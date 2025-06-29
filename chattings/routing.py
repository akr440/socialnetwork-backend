# chat/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/groupchat/(?P<group_id>\w+)/$', consumers.GroupChatConsumer.as_asgi()),
]