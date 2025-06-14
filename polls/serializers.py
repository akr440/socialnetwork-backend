from rest_framework import serializers
from .models import Polls, PollOptions, Votes


class PollOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollOptions
        fields = ['id', 'option_text']


class PollSerializer(serializers.ModelSerializer):
    options = PollOptionSerializer(many=True)
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Polls
        fields = ['id', 'question', 'created_at','user', 'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        poll = Polls.objects.create(**validated_data)
        for option_data in options_data:
            PollOptions.objects.create(poll=poll, **option_data)
        return poll


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votes
        fields = ['id', 'user', 'poll', 'option']

    def validate(self, data):
        if Votes.objects.filter(user=data['user'], poll=data['poll']).exists():
            raise serializers.ValidationError("You have already voted on this poll.")
        return data
