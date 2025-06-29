# chat/consumers.py

from channels.generic.websocket import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Chatroom, Message, GroupChatroom, GroupMessage
import json

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        self.room_name = self.scope['url_route']['kwargs']['room_id'] # room_id is passed from the frontend, when they 
        #request for a websocket connection after creating a chat...when they create a chat with a user..backend sends them 
        #the room_id, which they use to open websocket connection
        self.room_group_name = f"chat_{self.room_name}"
        self.user=self.scope['user']
        print(self.user)

        # Join group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_disconnect(self, event):
        # Leave group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def websocket_receive(self, event):    #this func is called when the client who opened the connection sends a message
        print(f"the event we get is :{event}")
        data = event.get("text",None)
        data=json.loads(data)
        message=data['message']
        print(message)

         # Broadcast to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',     #determines which method of the channels in the group will handle the broadcasted event
                'message': message,
                'sender': self.user.username,
            }
        )
     

        await self.save_message(self.user,message)

    async def chat_message(self, event):
       print(event)
       message=event['message']
       sender=event['sender']
       await self.send({
        "type" : "websocket.send",
        "text":json.dumps({
           'message':message,
           'sender':sender
       })})

    @database_sync_to_async
    def save_message(self, sender, content):
        try:
            chatroom = Chatroom.objects.get(pk=self.room_name)
        except Chatroom.DoesNotExist:
            return  # Or handle it with a log/error

        Message.objects.create(
            chatroom=chatroom,
            sender=sender,
            content=content
        )


class GroupChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        self.group_id=self.scope['url_route']['kwargs']['group_id']
        self.room_group_name=f"group_{self.group_id}"
        self.user=self.scope['user']
        print(self.user)

        # Join group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_disconnect(self, event):
        # Leave group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def websocket_receive(self, event):
        data = event.get("text", None)
        data = json.loads(data)
        message = data['message']
        print(message)

        # Broadcast to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'group_chat.message',
                'message': message,
                'sender': self.user.username,
            }
        )

        await self.save_message(self.user, message)
    
    async def group_chat_message(self, event):
        print(event)
        message = event['message']
        sender = event['sender']
        await self.send({
            "type": "websocket.send",
            "text": json.dumps({
                'message': message,
                'sender': sender
            })
        })

    @database_sync_to_async
    def save_message(self, sender, content):
        try:
            group_chatroom = GroupChatroom.objects.get(pk=self.group_id)
        except GroupChatroom.DoesNotExist:
            return
        GroupMessage.objects.create(
            group_chatroom=group_chatroom,
            sender=sender,
            content=content
        )

    