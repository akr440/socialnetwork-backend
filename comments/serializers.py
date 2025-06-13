from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')  # Fetches the username of the owner
    is_owner=serializers.SerializerMethodField()


    def get_is_owner(self,obj):
        return obj.owner==self.context["request"].user
    class Meta:
        model = Comment
        fields = [
            'id', 'owner', 'post', 'created_at', 'updated_at', 'content','is_owner',
        ]
        read_only_fields = ['id', 'owner', 'post', 'created_at']  # Exclude 'updated_at' from read-only
