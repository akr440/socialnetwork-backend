from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,APIView
from .import serializers
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
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
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            tokens = {"access": str(refresh.access_token), "refresh": str(refresh)}
            response = {"message": "Login Successfull", "user": user.username,"user_id":user.id,"tokens":tokens}
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Invalid email or password"})
        

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the refresh token from the request
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(
                {"error": "Invalid token or already blacklisted"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
