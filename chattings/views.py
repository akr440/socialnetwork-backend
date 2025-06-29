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
    # def post(self,request:Request,chatroom_id:int):
    #     data=request.data
    #     data['sender'] = request.user.id
    #     data['chatroom'] = chatroom_id
    #     serialize=serializers.MessageSerializer(data=data)
    #     if serialize.is_valid():
    #         serialize.save(sender=request.user,chatroom_id=chatroom_id)
    #         return Response(data=serialize.data,status=status.HTTP_201_CREATED)
    #     return Response(data=serialize.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request:Request,chatroom_id:int):
        history=models.Chatroom.objects.filter(id=chatroom_id)
        print(history)
        serialize=serializers.ChatroomSerializer(instance=history,many=True)
        return Response(data=serialize.data,status=status.HTTP_200_OK)

    
class CreateAndFetchGroupChatroom(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self,request:Request): #create a group chatroom
        data=request.data
        # data['created_by']=request.user.id
        serialize=serializers.GroupChatroomSerializer(data=data)
        if serialize.is_valid():
            serialize.save(created_by=request.user)
            return Response(data=serialize.data,status=status.HTTP_201_CREATED)
        return Response(data=serialize.errors,status=status.HTTP_400_BAD_REQUEST)

    def get(self,request:Request): #returns all the group chatrooms that the user is a member of
        rooms=models.GroupChatroom.objects.filter(members=request.user)
        serialize=serializers.GroupChatroomSerializer(instance=rooms,many=True)
        return Response(data=serialize.data,status=status.HTTP_200_OK)
    
class AddMember(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self,request:Request,group_id:int): #add a member to the group chatroom
        group=get_object_or_404(models.GroupChatroom,id=group_id)
        if request.user not in group.members.all():
            return Response(data={"message":"You are not a member of this group"},status=status.HTTP_403_FORBIDDEN)
        if request.user != group.created_by:
            return Response(data={"message":"Only the group creator can add members"},status=status.HTTP_403_FORBIDDEN)
        data=request.data
        user_to_add=get_object_or_404(User,id=data['user_id'])
        group.members.add(user_to_add)
        group.save()
        return Response(data={"message":"User added successfully"},status=status.HTTP_200_OK)
    
    
class GetGroup(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request:Request,group_id:int): #get the details of a group chatroom
        group=get_object_or_404(models.GroupChatroom,id=group_id)
        if request.user not in group.members.all():
            return Response(data={"message":"You are not a member of this group"},status=status.HTTP_403_FORBIDDEN)
        serialize=serializers.GroupChatroomSerializer(instance=group)
        return Response(data=serialize.data,status=status.HTTP_200_OK)

class RemoveMember(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self,request:Request,group_id:int): #remove a member from the group chatroom
        group=get_object_or_404(models.GroupChatroom,id=group_id)
        if request.user not in group.members.all():
            return Response(data={"message":"You are not a member of this group"},status=status.HTTP_403_FORBIDDEN)
        if request.user != group.created_by:
            return Response(data={"message":"Only the group creator can remove members"},status=status.HTTP_403_FORBIDDEN)
        data=request.data
        user_to_remove=get_object_or_404(User,id=data['user_id'])
        group.members.remove(user_to_remove)
        group.save()
        return Response(data={"message":"User removed successfully"},status=status.HTTP_200_OK)
    
class ExitGroup(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self,request:Request,group_id:int): #leave a group chatroom
        group=get_object_or_404(models.GroupChatroom,id=group_id)
        if request.user not in group.members.all():
            return Response(data={"message":"You are not a member of this group"},status=status.HTTP_403_FORBIDDEN)
        group.members.remove(request.user)
        group.save()
        return Response(data={"message":"You have left the group successfully"},status=status.HTTP_200_OK)
    
class GetGroupMessages(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request:Request,group_id:int): #get all messages of a group chatroom
        group=get_object_or_404(models.GroupChatroom,id=group_id)
        if request.user not in group.members.all():
            return Response(data={"message":"You are not a member of this group"},status=status.HTTP_403_FORBIDDEN)
        messages=group.messages.all()  # Fetch all messages related to the group chatroom, due to related_name='messages' in GroupMessage model
        #it allows us to access all messages related to the group chatroom directly
        serialize=serializers.GroupMessageSerializer(instance=messages,many=True)
        return Response(data=serialize.data,status=status.HTTP_200_OK)