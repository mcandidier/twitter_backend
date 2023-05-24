
from django.urls import re_path, path
from .consumers import NotificationConsumer
from .views import NotificationAPIView

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
]

urlpatterns = [
    path('', NotificationAPIView.as_view()),
]