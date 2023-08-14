from rest_framework import serializers
from .models import Profile, Tweet, Comment, Following

class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'location', 'birth_date', 'followers', 'following', 'username', 'avatar',]
        read_only_fields = ('followers', 'following', 'user',)


    def get_username(self, obj):
       return obj.user.username

    def get_following(self, obj):
        following_list = obj.user.following.values_list('following_id', flat=True)
        return list(following_list)

    def get_followers(self, obj):
        following_list = obj.user.followers.values_list('user_id', flat=True)
        return list(following_list)

    # def get_following(self, obj):
    #     return obj.user.following.all().count()
    

class TweetSerializer(serializers.ModelSerializer):
    
    username = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = ['id', 'user', 'content', 'created_at', 'likes', 'username'
        ]
        read_only_fields = ('likes', 'user',)

    def get_username(self, obj):
        return obj.user.username
    

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'tweet', 'content', 'created_at']
        read_only_fields = ('user',)


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('avatar',)