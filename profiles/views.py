from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,APIView
from .import serializers
from .import models


class ListProfile(APIView):
    def get(self,request:Request):
        profiles=models.Profile.objects.all()
        serialize=serializers.ProfileSerialsize(instance=profiles,many=True)
        response={
            "message":"profiles",
            "profiles":serialize.data
        }
        return Response(data=response,status=status.HTTP_200_OK)
    
class ProfileDetails(APIView):
    def get(self,request:Request,pk:int):
        profile=get_object_or_404(models.Profile,pk=pk)
        serialize=serializers.ProfileSerialsize(instance=profile)
        response={
            "message":"Profile Details",
            "data":serialize.data
        }
        return Response(data=response,status=status.HTTP_200_OK)
    
    def put(self,request:Request,pk:int):
        profile=get_object_or_404(models.Profile,pk=pk)
        updated_data=request.data
        serialize=serializers.ProfileSerialsize(profile,data=updated_data,partial=True)
        if serialize.is_valid():
            serialize.save()
            response={
                "message":"Successfully updated the profile",
                "profile data":serialize.data
            }
            return Response(data=response,status=status.HTTP_200_OK)
        return Response(data=serialize.errors,status=status.HTTP_400_BAD_REQUEST)