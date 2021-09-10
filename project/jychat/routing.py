from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/jychat/<room_name>/', consumers.JYChatConsumer.as_asgi()),
    path('ws/get/dblist/', consumers.ChatList.as_asgi()) # 챗 목록을 반환하는 WS 만들어 보자
]