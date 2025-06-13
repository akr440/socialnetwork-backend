from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,APIView
from .import serializers
from .import models
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly

class PostLists(APIView):
    permission_classes=[AllowAny]
    def get(self,request:Request):
        posts=models.Post.objects.all()
        serialize=serializers.PostSerialsize(instance=posts,many=True,context={"request":request})
        response={
            "message":"List of all Posts",
            "posts":serialize.data
        }
        return Response(data=response,status=status.HTTP_200_OK)
    
class CreatePost(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request:Request):
        data=request.data
        print(f"input data for post:{data}")
        serialize=serializers.PostSerialsize(data=data,context={"request":request})
        if serialize.is_valid():
            serialize.save()
            response={
                "message":"Post created.",
                "Post":serialize.data
            }
            return Response(data=response,status=status.HTTP_201_CREATED)
        return Response(data=serialize.errors,status=status.HTTP_400_BAD_REQUEST)

class PostDetailnUpdate(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly]
    def get(self,request:Request,pk:int):
        post=get_object_or_404(models.Post,pk=pk)
        serialize=serializers.PostSerialsize(instance=post,context={"request":request})
        response={
            "message":"Post Details fetched",
            "Details":serialize.data
        }
        return Response(data=response,status=status.HTTP_200_OK)
    
    def put(self,request:Request,pk:int):
        updated_data=request.data
        post=get_object_or_404(models.Post,pk=pk)
        if post.owner_id!=request.data["user_id"]:
            return Response(data={"message":"Action denied"},status=status.HTTP_403_FORBIDDEN)
        serialize=serializers.PostSerialsize(post,data=updated_data,partial=True,context={"request":request})
        if serialize.is_valid():
            serialize.save()
            response={
                "message":"Succesfully Updated",
                "Post":serialize.data
            }
            return Response(data=response,status=status.HTTP_200_OK)
        return Response(data=serialize.errors,status=status.HTTP_400_BAD_REQUEST)