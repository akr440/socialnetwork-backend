from rest_framework import serializers
from .models import Chatroom,Message


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