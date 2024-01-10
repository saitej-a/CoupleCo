from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from django.contrib.auth.models import User
from .models import Room,Messages
from pytube import YouTube
from googleapiclient.discovery import build

class Chatconsumer(WebsocketConsumer):
    def connect(self):
        
        self.room_id=self.scope['url_route']['kwargs']['pk']
        
        
        async_to_sync(self.channel_layer.group_add)(self.room_id,self.channel_name)
        self.accept()
    def disconnect(self, code):
        print('disconnect')
        async_to_sync(self.channel_layer.group_discard)(self.room_id,self.channel_name)
    
    def receive(self, text_data=None, bytes_data=None):
        text_data_json=json.loads(text_data)
        #print(text_data_json)
        message=text_data_json['message']
        user= text_data_json['username']
        Messages.objects.create(room=Room.objects.get(id=self.room_id),sender=User.objects.get(username=user),body=message)
        async_to_sync(self.channel_layer.group_send)(self.room_id,{'type':'sendback','message':message,'username':user})
        
    def sendback(self,event):
        message=event['message']
        username=event['username']

        self.send(text_data=json.dumps({'message':message,'username':username}))

class videoConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id='video'+self.scope['url_route']['kwargs']['pk']
        async_to_sync(self.channel_layer.group_add)(self.room_id,self.channel_name)

        self.accept()
        
    def disconnect(self,code):
        async_to_sync(self.channel_layer.group_discard)(self.room_id,self.channel_name)
    def receive(self, text_data=None, bytes_data=None):
        text_data_json=json.loads(text_data)
        state=text_data_json['state']
        async_to_sync(self.channel_layer.group_send)(self.room_id,{'type':'retur','state':state})
    def retur(self,event):
        state=event['state']
        
        self.send(text_data=json.dumps({'state':state}))

class getresults(WebsocketConsumer):
    def connect(self):
        self.room_id='chat'+self.scope['url_route']['kwargs']['pk']
        async_to_sync(self.channel_layer.group_add)(self.room_id,self.channel_name)
        self.accept()
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.room_id,self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json=json.loads(text_data)
        title=text_data_json['title']
        async_to_sync(self.channel_layer.group_send)(self.room_id, { 'type' : 'reff','title':title})
    def reff(self,event):
        title=event['title']
        
        
        api_service_name = "youtube"
        api_version = "v3"
        key="AIzaSyCYaeAMaCLGv2iXwBLi2Zy2r91PBD6l-IU"
        youtube = build(
            api_service_name,
            api_version,developerKey=key)
        request = youtube.search().list(q=title,part="snippet",maxResults=10)
        response1 = request.execute()
        # print(response1)
        # streamable=''
        # for i in response1['items']:
        #     if i['id']['kind']!='youtube#playlist':
                
        #         link=YouTube(i['id']['videoId'])
        #         streamable +=link.streams.get_lowest_resolution().url
        #     else:
        #         continue
        
        self.send(text_data=json.dumps({'responce':response1}))
        

class selected(WebsocketConsumer):
    def connect(self):
        self.room_id="select"+self.scope['url_route']['kwargs']['pk']
        async_to_sync(self.channel_layer.group_add)(self.room_id,self.channel_name)
        self.accept()
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.room_id,self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json=json.loads(text_data)
        i=text_data_json['id']
        url1='https://youtu.be/'+i
        link=YouTube(url1)
        streamable =link.streams.get_lowest_resolution().url
        
        async_to_sync(self.channel_layer.group_send)(self.room_id,{'type':'nun','streamlink':streamable})
    def nun(self,event):
        streamlink=event['streamlink']
        self.send(text_data=json.dumps({'streamlink':streamlink}))
