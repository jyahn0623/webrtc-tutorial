from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('webrtc/', consumers.ChatConsumer.as_asgi()),
]