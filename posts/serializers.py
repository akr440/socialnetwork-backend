from rest_framework import serializers
from .models import Post
from rest_framework.validators import ValidationError

class PostSerialsize(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner=serializers.SerializerMethodField()


    def get_is_owner(self,obj):
        return obj.owner==self.context["request"].user
    
    class Meta:
        model = Post
        # to list all fields all in an array or set to '__all__'  
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'title',
            'content','is_owner'
        ]
    
    def create(self, validated_data):
        # Automatically set the owner field
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)