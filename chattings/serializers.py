from rest_framework import serializers
from .models import Chatroom,Message,GroupChatroom,GroupMessage
from accounts.models import User


class MessageSerializer(serializers.ModelSerializer):
    sender=serializers.ReadOnlyField(source='sender.username') 

    class Meta:
        model=Message
        fields=[
            'id','content','sender','chatroom','created_at',
        ]
        



class ChatroomSerializer(serializers.ModelSerializer):
    user1 = serializers.ReadOnlyField(source='user1.username')  # Fetches the username of the owner
    user2 = serializers.ReadOnlyField(source='user2.username')  
    messages=MessageSerializer(many=True,read_only=True) #drf automatically fetches all the related messages with the particular chatroom, this is because 
#the related_names = messages that we implemented while creating the Message model,
    
    class Meta:
        model = Chatroom
        fields = [
            'id', 'created_at', 'user1', 'user2','messages',
        ]

class GroupChatroomSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')  # Fetches the username of the creator
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    class Meta:
        model = GroupChatroom
        fields = [
            'id', 'name', 'members', 'created_at', 'created_by',
        ]

    def create(self, validated_data):
        members = validated_data.pop('members', [])   #- ManyToManyField relationships must be set after the object is created.
        group_chatroom = super().create(validated_data)
        group_chatroom.members.set(members)
        group_chatroom.members.add(validated_data['created_by'])
        group_chatroom.save()
        return group_chatroom
    
class GroupMessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')
    group_chatroom = serializers.ReadOnlyField(source='group_chatroom.name')

    class Meta:
        model = GroupMessage
        fields = [
            'id', 'content', 'sender', 'group_chatroom', 'created_at',
        ]