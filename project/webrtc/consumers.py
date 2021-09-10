from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group = f'chat_test'

        await self.channel_layer.group_add(
            self.group,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group,
            self.channel_name
        )

    async def receive(self, text_data):
        # print(text_data) # "peer":"test","action":"new-peer","message":{}}
        recieve_dict = json.loads(text_data)
        message = recieve_dict.get('message')
        action = recieve_dict.get('action')

        # print(message, action)

        if action == 'new-offer' or action == 'new-answer':
            receiever_channel_name = recieve_dict['message']['receiever_channel_name']

            recieve_dict['message']['receiever_channel_name'] = self.channel_name 
            await self.channel_layer.send(
                receiever_channel_name,
                {
                    'type' : 'send.sdp',
                    'receive_dict' : recieve_dict
                }
            )
            return

        recieve_dict['message']['receiever_channel_name'] = self.channel_name

        await self.channel_layer.group_send(
            self.group,
            {
                'type' : 'send.sdp',
                'receive_dict' : recieve_dict
            }
        )

    async def send_sdp(self, e):
        receive_dict = e.get('receive_dict')
        await self.send(text_data=json.dumps(receive_dict))
