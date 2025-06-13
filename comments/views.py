from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,APIView
from .import serializers
from .import models
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly

class AllCommentsListNCreate(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly]
    def get(self,request:Request,post_id:int):
        comments=models.Comment.objects.filter(post_id=post_id)
        serializer=serializers.CommentSerializer(instance=comments,many=True,context={"request":request})
        response={
            "message":"Comments fetched",
            "comments":serializer.data
        }
        return Response(data=response,status=status.HTTP_200_OK)
    
    def post(self,request:Request,post_id:int):
        comment_data=request.data
        serialize=serializers.CommentSerializer(data=comment_data,context={"request":request})
        if serialize.is_valid():
            serialize.save(owner=request.user,post_id=post_id)
            response={
                "message":"comment added",
                "comment data":serialize.data
            }
            return Response(data=response,status=status.HTTP_201_CREATED)
        return Response(data=serialize.errors,status=status.HTTP_400_BAD_REQUEST)


class CommentDetailNUpdate(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly]
    def get(self,request:Request,pk:int):
        comment=get_object_or_404(models.Comment,pk=pk)
        serializer=serializers.CommentSerializer(instance=comment,context={"request":request})
        response={
            "message":"Comment fetched",
            "comments":serializer.data
        }
        return Response(data=response,status=status.HTTP_200_OK)
    def put(self,request:Request,pk:int):
        comment=get_object_or_404(models.Comment,id=pk)
        print(f"owner is :{comment.owner}")
        print(f"user is :{request.user}")
        if comment.owner!=request.user:
            return Response(data={"message":"Permission Denied"},status=status.HTTP_403_FORBIDDEN)
        
        updated_comment=request.data
        serialize=serializers.CommentSerializer(comment,data=updated_comment,partial=True,context={"request":request})
        if serialize.is_valid():
            serialize.save()
            response={
                "message":"Comment edited",
                "new comment":serialize.data
            }
            return Response(data=response,status=status.HTTP_200_OK)
        return Response(data=serialize.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request:Request,pk:int):
        comment=get_object_or_404(models.Comment,id=pk)
        print(f"owner is :{comment.owner}")
        print(f"user is :{request.user}")
        if comment.owner!=request.user:
            return Response(data={"message":"Permission Denied"},status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(data={"message":"Comment deleted"},status=status.HTTP_204_NO_CONTENT)

