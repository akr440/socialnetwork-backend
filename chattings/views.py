from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,APIView
from .import serializers
from .import models
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from accounts.models import User
import pprint
class CreateChatroom(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request:Request,user_id:int):
        to_user=User.objects.get(id=user_id)
        if request.user==to_user:
            return Response(data={"Message":"you cannot create room with yourself"},status=status.HTTP_403_FORBIDDEN)
        chatroom = models.Chatroom.objects.filter(
                    (Q(user1_id=user_id) & Q(user2_id=request.user.id)) | (Q(user1_id=request.user.id) & Q(user2_id=user_id))
                ).first()
        if chatroom:
            serialize=serializers.ChatroomSerializer(chatroom)
            return Response(data=serialize.data,status=status.HTTP_200_OK)

        data={"user1_id":request.user.id,"user2_id":user_id}
        serialize=serializers.ChatroomSerializer(data=data)
        if serialize.is_valid():
            serialize.save(user1_id=request.user.id,user2_id=user_id)
            return Response(data=serialize.data,status=status.HTTP_201_CREATED)
        return Response(data=serialize.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
class getChatrooms(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request:Request):
        rooms=models.Chatroom.objects.filter(user1=request.user)|models.Chatroom.objects.filter(user2=request.user)
        serialize=serializers.ChatroomSerializer(instance=rooms,many=True)
        return Response(data=serialize.data,status=status.HTTP_200_OK)

class SendMessage(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request:Request,chatroom_id:int):
        data=request.data
        data['sender'] = request.user.id
        data['chatroom'] = chatroom_id
        serialize=serializers.MessageSerializer(data=data)
        if serialize.is_valid():
            serialize.save(sender=request.user,chatroom_id=chatroom_id)
            return Response(data=serialize.data,status=status.HTTP_201_CREATED)
        return Response(data=serialize.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request:Request,chatroom_id:int):
        history=models.Chatroom.objects.filter(id=chatroom_id)
        print(history)
        serialize=serializers.ChatroomSerializer(instance=history,many=True)
        return Response(data=serialize.data,status=status.HTTP_200_OK)

    
