import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat_{self.room_name}'
#         """
#         self.scope 데이터
#         {'type': 'websocket', 'path': '/ws/main/lobby/', 'raw_path': b'/ws/main/lobby/', 'headers': [(b'host', b'127.0.0.1:8000'), (b'connection', b'Upgrade'), (b'pragma', b'no-cache'), (b'cache-control', b'no-cache'), (b'user-agent', b'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'), (b'upgrade', b'websocket'), (b'origin', b'http://127.0.0.1:8000'), (b'sec-websocket-version', b'13'), (b'accept-encoding', b'gzip, deflate, br'), (b'accept-language', b'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'), (b'sec-websocket-key', b'dZdk3u63NLSvQ0Com2bGwA=='), (b'sec-websocket-extensions', b'permessage-deflate; client_max_window_bits')], 'query_string': 
#         b'', 'client': ['127.0.0.1', 61409], 'server': ['127.0.0.1', 8000], 'subprotocols': [], 
#         'asgi': {'version': '3.0'}, 'cookies': {}, 'session': <django.utils.functional.LazyObject object at 0x000002BD48A894E0>, 'user': <channels.auth.UserLazyObject object at 0x000002BD48A891D0>, 'path_remaining': '', 'url_route': {'args': (), 'kwargs': {'room_name': 'lobby'}}}
#         """

#         # 방 그룹에 넣어보리기 
#         # print(self.channel_name) # specific.c8d25044e745473f8c7bbae5b4860d09!a154565f931846329cce7b2b79b6dd1b  
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name # 그룹에 해당 ChatConsumer의 인스턴스를 추가해 버림.
#         ) # redis 채널 레이어의 인터페이스를 사용하기 위해 설치했지?

#         self.accept() # 이 놈 안 쓰면 연결 거부

#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # 같은 클라이언트에게 보내는 코드 like that
#         # 같은 룸에 있는 모든 사람들에게 보내야지?
#         # self.send(text_data=json.dumps({
#         #     'message': message
#         # }))

#         # 그룹에게 보낸다.
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type' : 'chat_message',
#                 'message' : message,
#             }
#         )
    
#     def chat_message(self, event): # 이 녀석은 위의 type의 핸들러인 듯. 이름이 똑같아야 함.
#         # print(event) # {'type': 'chat_message', 'message': '안녕'}
#         message = event['message']

#         # 웹소켓에 메세지 보내기
#         self.send(text_data=json.dumps({
#             'message' : message
#         }))

# 퍼포먼스 향상을 위해 비동기적으로 다시 컨슈머를 구성할 필요가 있음.
from channels.generic.websocket import AsyncWebsocketConsumer
class ChatConsumer(AsyncWebsocketConsumer):
    # async, await 가 붙네여~ js인가요?
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        """
        self.scope 데이터
        {'type': 'websocket', 'path': '/ws/main/lobby/', 'raw_path': b'/ws/main/lobby/', 'headers': [(b'host', b'127.0.0.1:8000'), (b'connection', b'Upgrade'), (b'pragma', b'no-cache'), (b'cache-control', b'no-cache'), (b'user-agent', b'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'), (b'upgrade', b'websocket'), (b'origin', b'http://127.0.0.1:8000'), (b'sec-websocket-version', b'13'), (b'accept-encoding', b'gzip, deflate, br'), (b'accept-language', b'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'), (b'sec-websocket-key', b'dZdk3u63NLSvQ0Com2bGwA=='), (b'sec-websocket-extensions', b'permessage-deflate; client_max_window_bits')], 'query_string': 
        b'', 'client': ['127.0.0.1', 61409], 'server': ['127.0.0.1', 8000], 'subprotocols': [], 
        'asgi': {'version': '3.0'}, 'cookies': {}, 'session': <django.utils.functional.LazyObject object at 0x000002BD48A894E0>, 'user': <channels.auth.UserLazyObject object at 0x000002BD48A891D0>, 'path_remaining': '', 'url_route': {'args': (), 'kwargs': {'room_name': 'lobby'}}}
        """

        # 방 그룹에 넣어보리기 
        # print(self.channel_name) # specific.c8d25044e745473f8c7bbae5b4860d09!a154565f931846329cce7b2b79b6dd1b  
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name # 그룹에 해당 ChatConsumer의 인스턴스를 추가해 버림.
        ) # redis 채널 레이어의 인터페이스를 사용하기 위해 설치했지?

        await self.accept() # 이 놈 안 쓰면 연결 거부

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # 같은 클라이언트에게 보내는 코드 like that
        # 같은 룸에 있는 모든 사람들에게 보내야지?
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))

        # 그룹에게 보낸다.
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'chat_message',
                'message' : message,
            }
        )
    
    async def chat_message(self, event): # 이 녀석은 위의 type의 핸들러인 듯. 이름이 똑같아야 함.
        # print(event) # {'type': 'chat_message', 'message': '안녕'}
        message = event['message']

        # 웹소켓에 메세지 보내기
        await self.send(text_data=json.dumps({
            'message' : message
        }))
