from rest_framework import serializers
from .models import Follow

class FollowSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    followed_user=serializers.ReadOnlyField(source='followed_user.username')

    class Meta:
        model = Follow
        fields = ['id', 'user', 'followed_user', 'created_at']
