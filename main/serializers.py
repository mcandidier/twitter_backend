from rest_framework import serializers
from .models import Profile, Tweet, Comment

class ProfileSerializer(serializers.ModelSerializer):

    followers = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'location', 'birth_date', 'followers']
        read_only_fields = ('followers', 'user',)

    def get_followers(self, obj):
        return obj.user.followers.all().count()

class TweetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tweet
        fields = ['id', 'user', 'content', 'created_at', 'likes']
        read_only_fields = ('likes', 'user',)



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'tweet', 'content', 'created_at']
        read_only_fields = ('user',)