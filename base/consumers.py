from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async
import json

class Chatconsumer(WebsocketConsumer):
    async def connect(self):
        print(self.scope['url_route']['kwargs']['pk'])
        self.room_id=self.scope['url_route']['kwargs']['pk']
        
        self.room_groupid="room_"+self.room_id
        await self.channel_layer.group_add(self.room_id,self.room_groupid)
        await self.accept()
    async def disconnect(self, code):
        print('disconnect')
        await self.channel_layer.group_discard(self.room_id,self.room_groupid)
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json=json.loads(text_data)
        message=text_data_json['message']
        user= text_data_json['username']
        await sync_to_async(self.channel_layer.group_add(self.room_groupid,{'message':message,'username':user,'type':'sendback'}))
    
    async def sendback(self,event):
        message=event['message']
        username=event['usernamee']
        await self.send(text_data=json.dumps({'message':message,'username':username}))
    