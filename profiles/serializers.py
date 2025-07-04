from rest_framework import serializers
from .models import Profile
from rest_framework.validators import ValidationError

class ProfileSerialsize(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner=serializers.SerializerMethodField()


    def get_is_owner(self,obj):
        return obj.owner==self.context["request"].user
    
    class Meta:
        model = Profile
        # to list all fields all in an array or set to '__all__'  
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name','dob',
            'content','is_owner',
        ]