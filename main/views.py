import os
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage


from .serializers import (
    ProfileSerializer, 
    TweetSerializer, 
    CommentSerializer,
    UserImageSerializer,
    )
from .models import Profile, Tweet, Comment, Following, Like


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    @action(methods=['post'], detail=True)
    def follow(self, request, pk=None):
        instance = self.get_object()
        action_type = request.data.get('action')
        msg = ''
        try:
            if action_type == 'follow':
                Following.objects.create(
                    user=self.request.user,
                    following=instance.user
                )
                msg = 'followed'
            else:
                obj = Following.objects.filter(
                    user=self.request.user,
                    following=instance.user)
                if obj.exists():
                    obj.first().delete()
                msg = 'unfollow'
        except Exception as exc:
            return Response({'msg': exc}, status=400)
        return Response({'msg': msg}, status=200)
    

class UserProfileViewSet(viewsets.ViewSet):
    serializer_class = ProfileSerializer
    
    def retrieve(self, *args, **kwargs): 
        try:
            user_id = kwargs.get('id')
            obj = Profile.objects.get(user__id=user_id)
            serializer = self.serializer_class(obj)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({'msg': 'object not found'}, status=400)
        
    def update_profile(self, *args, **kwargs):
        try:
            user_profile = Profile.objects.get(user=self.request.user)
            serializer = self.serializer_class(user_profile, data=self.request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({'msg': 'object not found'}, status=400)


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def perform_create(self, serializer):
        serializer = serializer.save(user=self.request.user)
        return super().perform_create(serializer)

    @action(methods=['get'], detail=True)
    def comments(self, request, pk=None):
        queryset = Comment.objects.filter(tweet__pk=pk)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    @action(methods=['post'], detail=True, url_path='likes')
    def likes(self, request, pk=None):
        instance = self.get_object()
        Like.objects.create(user=self.request.user, tweet=instance)
        return Response({'msg': 'success'}, status=200)

    @action(methods=['delete'], detail=True, url_path='unlike')
    def unlike(self, request, pk=None):
        instance = self.get_object()
        try:
            instance.likes.delete(self.request.user)
        except Exception as e:
            print(e)
        return Response({'msg': 'success'}, status=200)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # form data: tweet_id, content
        serializer = serializer.save(user=self.request.user)
        return super().perform_create(serializer)


class FollowViewSet(viewsets.ViewSet):

    def follow(self, *args, **kwargs):
        pass


class UserUploadImageView(APIView):
    """Upload user profile image
    """
    parser_classes = (MultiPartParser,)
    
    def put(self, format=None):
        profile = self.request.user.profile
        serializer  = UserImageSerializer(profile, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)



