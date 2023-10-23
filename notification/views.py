from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import permissions


from .models import Notification
from .serializers import NotificationSerializer
from .permissions import IsOwnerOrReadOnly


class NotificationAPIView(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self, *args, **kwargs):
        return Notification.objects.filter(user=self.request.user)


class MarkNotificationAsRead(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request, notification_id):
        notification = get_object_or_404(Notification, pk=notification_id)
        notification.read = True
        notification.save()
        return Response({'message': 'Notification marked as read'}, status=status.HTTP_200_OK)
