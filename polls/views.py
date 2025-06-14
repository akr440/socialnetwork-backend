from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,APIView
from .import serializers
from .import models
from accounts.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from pprint import pprint

class CreatePoll(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request:Request):
        data=request.data
        serialize=serializers.PollSerializer(data=data)
        if serialize.is_valid():
            serialize.save(user=request.user)
            response={
                "message":"Poll created",
                "poll":serialize.data
            }
            return Response(data=response,status=status.HTTP_201_CREATED)
        return response(data=serialize.errors,status=status.HTTP_400_BAD_REQUEST)
    

class VoteinPoll(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request:Request,poll_id:int):
        data={**request.data,"user":request.user.id,"poll":poll_id}
        pprint(vars(request))
        poll=models.Polls.objects.get(id=poll_id)
        serialize=serializers.VoteSerializer(data=data)
        if serialize.is_valid():
            serialize.save()
            response={
                "message":"Vote created",
                "poll":serialize.data
            }
            return Response(data=response,status=status.HTTP_201_CREATED)
        return Response(data=serialize.errors,status=status.HTTP_400_BAD_REQUEST)
    
class getPoll(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request:Request,poll_id:int):
        poll=get_object_or_404(models.Polls,id=poll_id)
        serialize=serializers.PollSerializer(instance=poll)
        return Response(serialize.data, status=status.HTTP_200_OK)
    

class DeletPoll(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request:Request,poll_id:int):
        poll=models.Polls.objects.get(id=poll_id)
        if request.user.id!=poll.user_id:
            return Response(data={"message":"Permission denied"},status=status.HTTP_403_FORBIDDEN)
        poll.delete()
        return Response(data={"Poll deleted"},status=status.HTTP_204_NO_CONTENT)