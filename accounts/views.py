from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,APIView
from .import serializers
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
# from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

class UserSignup(APIView):

    serializer_class=serializers.SignupSerialsize
    def post(self,request:Request):
        user_data=request.data
        print(f"Requested user data:{user_data}")
        serialize=serializers.SignupSerialsize(data=user_data)
        if serialize.is_valid():
            serialize.save()
            print(f"Serialized data:{serialize}")
            response={
                "message":"user signed up succesfully",
                "data":serialize.data
            }
            return Response(data=response,status=status.HTTP_201_CREATED)
        return Response(data=serialize.errors,status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    
    def post(self,request:Request):
        email=request.data.get("email")
        password=request.data.get("password")
        user=authenticate(email=email,password=password)
        print(f"user is {user}")
        if user is not None:
            response = {"message": "Login Successfull", "user": user.username}
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Invalid email or password"})

