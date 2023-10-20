
from django.urls import re_path, path
from .views import NotificationAPIView
# from .consumers import NotificationConsumer
# websocket_urlpatterns = [
#     re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
# ]

urlpatterns = [
    path('', NotificationAPIView.as_view()),
]