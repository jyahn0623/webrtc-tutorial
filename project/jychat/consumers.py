import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from .models import * 

class JYChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # print(self.scope.get('user')) user 접근 가능
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.group,
            self.channel_name
        )

        await self.accept() # 연결 수립

        # 채팅방 연결되었습니다. 안내
        await self.channel_layer.group_send(
            self.group,
            {
                "type" : "enter_room",
                "user" : '띨띨한 오봉딜' # 닉네임은 변화를 주어야 할 듯?
            }
        )


    async def disconnect(self, close_code):
        # print(close_code) # 1001
        await self.channel_layer.group_discard(
            self.group,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        user = text_data_json.get('user')
        # print(self.group) # chat_lccksdf2

        await self.create_chat_message(message, user) # 채팅 내용 저장

        await self.channel_layer.group_send(
            self.group,
            {
                "type" : "chat_message",
                "message" : message,
                "user" : user
            }
        )
    
    # ValueError: No handler for message type chat_message 핸들러 만들어
    async def chat_message(self, event):
        message = event.get('message')
        user = event.get('user')

        await self.send(text_data=json.dumps({
            'message' : message,
            'user' : user
        }))

    async def enter_room(self, e):
        user = e.get('user')
        await self.send(text_data=json.dumps({
            'message' : f'{user}님이 입장하셨습니다.'
        }))

    @database_sync_to_async
    def create_chat_message(self, message, user):
        ChatMessage.objects.create(
            message=message,
            user=user
        )
    
class ChatList(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, closed_code):
        print('연결 종료')

    def receive(self, text_data):
        chatlists = list(ChatMessage.objects.order_by('-pk').values_list('user', 'message'))
        self.send(text_data=json.dumps({
            'chatlist' : chatlists
        }))