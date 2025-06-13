from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,APIView
from .import serializers
from .import models
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly

class ListLikes(APIView):
    permission_classes=[AllowAny]
    def get(self,request:Request,post_id:int):
        likes=models.Like.objects.filter(post_id=post_id)
        serialize=serializers.LikeSerializer(instance=likes,many=True)
        response={
            "message":"Likes fetched",
            "Likes":serialize.data
        }
        return Response(data=response,status=status.HTTP_200_OK)
    
class CreateDeleteLikes(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request:Request,post_id:int):
        if models.Like.objects.filter(user=request.user, post_id=post_id).exists():
            return Response(data={"message":"You have already liked this post"},status=status.HTTP_403_FORBIDDEN)
        data = {"post": post_id, "user": request.user}
        serialize=serializers.LikeSerializer(data=data)
        if serialize.is_valid():
            serialize.save(post_id=post_id, user= request.user)
            response={
                "message":"Liked",
                "data":serialize.data
            }
            return Response(data=response,status=status.HTTP_201_CREATED)
        return Response(data=serialize.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request:Request,post_id:int):

        like=models.Like.objects.filter(user=request.user,post_id=post_id)
        if not like:
            return Response({'detail': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response(data={"message":"Comment deleted"},status=status.HTTP_204_NO_CONTENT)

