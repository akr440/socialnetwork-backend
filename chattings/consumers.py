# chat/consumers.py

from channels.generic.websocket import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Chatroom, Message, GroupChatroom, GroupMessage, GroupMessageStatus, MessageStatus
from django.utils import timezone
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

        await self.mark_private_messages_as_read(self.user, self.room_name) # Mark all previous messages as read for this user in this chatroom
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

        # Save the message to the database
        msg = await self.save_message(self.user, message)
        if not msg:
            print("Failed to save message.")
            return

        # Broadcast to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',     #determines which method of the channels in the group will handle the broadcasted event
                'message': message,
                'sender': self.user.username,
                'message_id': msg.id
            }
        )
     

    async def chat_message(self, event):
       print(event)
       message=event['message']
       sender=event['sender']
       message_id=event['message_id']
       await self.send({
        "type" : "websocket.send",
        "text":json.dumps({
           'message':message,
           'sender':sender
       })})
       if sender != self.user.username:  # If the message is not sent by the current user, mark it as read
           await self.mark_singleprivate_messages_as_read(self.user, message_id)


    @database_sync_to_async
    def save_message(self, sender, content):
        try:
            chatroom = Chatroom.objects.get(pk=self.room_name)
        except Chatroom.DoesNotExist:
            return None

        message=Message.objects.create(
            chatroom=chatroom,
            sender=sender,
            content=content
        )
        for user in [chatroom.user1, chatroom.user2].exclude(id=sender.id):
            MessageStatus.objects.get_or_create( #get_or_create is used to avoid creating duplicate entries for the same message and user, because
                message=message,                  #in concurrent scenarios, retries to create the same row can happen
                user=user,
                defaults={'is_read': False}
            )
        return message
    
    @database_sync_to_async
    def mark_singleprivate_messages_as_read(self, user, message_id):
        MessageStatus.objects.filter(
            user=user,
            message_id=message_id,
            is_read=False
        ).update(
            is_read=True,
            read_at=timezone.now()
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
        # Mark all previous messages as read for this user in this group
        # This is done to ensure that when a user connects to the group chat, they see all messages as read
        await self.mark_group_messages_as_read(self.user, self.group_id)

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
        # Save the message to the database
        msg = await self.save_message(self.user, message)
        if not msg:
            raise ValueError("Failed to save message.")
        # Broadcast to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'group_chat.message',
                'message': message,
                'sender': self.user.username,
                'message_id': msg.id  # Include message ID for reference
            }
        )

    
    async def group_chat_message(self, event):
        print(event)
        message = event['message']
        sender = event['sender']
        message_id = event.get('message_id', None)  # Optional message ID if needed
        await self.send({
            "type": "websocket.send",
            "text": json.dumps({
                'message': message,
                'sender': sender
            })
        })

        if sender!=self.user.username:
            await self.mark_single_group_messages_as_read(self.user,message_id)

    @database_sync_to_async
    def save_message(self, sender, content):
        try:
            group_chatroom = GroupChatroom.objects.get(pk=self.group_id)
        except GroupChatroom.DoesNotExist:
            return None
        message=GroupMessage.objects.create(
            group_chatroom=group_chatroom,
            sender=sender,
            content=content
        )
        for member in group_chatroom.members.exclude(id=sender.id):
            GroupMessageStatus.objects.get_or_create(
                group_message=message,
                user=member,
                defaults={'is_read': False}
            )
        return message

    @database_sync_to_async
    def mark_single_group_messages_as_read(self, user, message_id):
        GroupMessageStatus.objects.filter(
            user=user,
            group_message_id=message_id,
            is_read=False
        ).update(
            is_read=True,
            read_at=timezone.now()
        )



    