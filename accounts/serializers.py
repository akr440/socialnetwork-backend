from rest_framework import serializers
from .models import User
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token

class SignupSerialsize(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email","password","username"]

    def validate(self, attrs):
            print(f"attrs value is {attrs}")

            email_exists = User.objects.filter(email=attrs["email"]).exists()

            if email_exists:
                raise ValidationError("Email has already been used")

            return super().validate(attrs)

    def create(self,val):  #for hashing the password, automatically takes the password at the time of storing it 
        #in the model and hash it before storing
        password = val.pop("password")

        user = super().create(val)

        user.set_password(password)

        user.save()
        return user