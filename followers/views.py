from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,APIView
from .import serializers
from .import models
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from accounts.models import User

class FollowUser(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request:Request,followed_user_id:int):
        id=User.objects.get(id=followed_user_id)
        print(f"username:{id.id}")
        print(f"current user:{request.user.id}")
        if id.id==request.user.id:
            return Response(data={"message":"You cant follow yourself"},status=status.HTTP_403_FORBIDDEN)
        data={"user":request.user,"followed_user_id":followed_user_id}
        serialize=serializers.FollowSerializer(data=data)
        if serialize.is_valid():
            serialize.save(user=request.user,followed_user_id=followed_user_id)
            response={
                "message":f"{followed_user_id} followed",
                "data":serialize.data
            }
            return Response(data=response,status=status.HTTP_201_CREATED)
        return Response(data=serialize.errors,status=status.HTTP_400_BAD_REQUEST)
    

class UnfollowUser(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request:Request,followed_user_id:int):
        id=User.objects.get(id=followed_user_id)
        print(f"username:{id.id}")
        print(f"current user:{request.user.id}")
        if id.id==request.user.id:
            return Response(data={"message":"You cant follow yourself"},status=status.HTTP_403_FORBIDDEN)
        obj=models.Follow.objects.filter(user=request.user,followed_user_id=followed_user_id)
        if not obj:
            return Response({'detail': 'You have not followed this user.'}, status=status.HTTP_400_BAD_REQUEST)

        obj.delete()
        return Response(data={"message":"Unfollowed user"},status=status.HTTP_204_NO_CONTENT)


class ListFollowing(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request:Request):
        following=models.Follow.objects.filter(user=request.user)
        serialize=serializers.FollowSerializer(instance=following,many=True)
        return Response(data=serialize.data,status=status.HTTP_200_OK)
    
class ListFollowers(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request:Request):
        followers=models.Follow.objects.filter(followed_user=request.user)
        serialize=serializers.FollowSerializer(instance=followers,many=True)
        return Response(data=serialize.data,status=status.HTTP_200_OK)
     
