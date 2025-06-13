from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,APIView
from .import serializers
from .import models
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly

class ListProfile(APIView):
    permission_classes =[AllowAny]
    def get(self,request:Request):
        profiles=models.Profile.objects.all()
        serialize=serializers.ProfileSerialsize(instance=profiles,many=True,context={"request":request})
        response={
            "message":"profiles",
            "profiles":serialize.data
        }
        return Response(data=response,status=status.HTTP_200_OK)
    
class ProfileDetails(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly]
    def get(self,request:Request,pk:int):
        profile=get_object_or_404(models.Profile,pk=pk)
        serialize=serializers.ProfileSerialsize(instance=profile,context={"request":request})
        response={
            "message":"Profile Details",
            "data":serialize.data
        }
        return Response(data=response,status=status.HTTP_200_OK)
    
    def put(self,request:Request,pk:int):
        profile=get_object_or_404(models.Profile,pk=pk)
        print(f"profile owner:{profile.owner_id}")
        print(f"request user:{request.data}")
        if profile.owner_id!=request.data["user_id"]:
            return Response(data={"message":"You cant modify others profile"},status=status.HTTP_403_FORBIDDEN)
        updated_data=request.data
        serialize=serializers.ProfileSerialsize(profile,data=updated_data,partial=True,context={"request":request})
        if serialize.is_valid():
            serialize.save()
            response={
                "message":"Successfully updated the profile",
                "profile data":serialize.data
            }
            return Response(data=response,status=status.HTTP_200_OK)
        return Response(data=serialize.errors,status=status.HTTP_400_BAD_REQUEST)