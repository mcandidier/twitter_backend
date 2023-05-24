from django.shortcuts import render
from rest_framework import generics

from .models import Notification
from .serializers import NotificationSerializer


class NotificationAPIView(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self, *args, **kwargs):
        return Notification.objects.filter(user=self.request.user)

