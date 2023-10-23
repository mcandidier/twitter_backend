
from django.urls import re_path, path
from .views import NotificationAPIView,MarkNotificationAsRead

# from .consumers import NotificationConsumer
# websocket_urlpatterns = [
#     re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
# ]

urlpatterns = [
    path('', NotificationAPIView.as_view()),
    path('<int:notification_id>/', MarkNotificationAsRead.as_view(), name='mark-notification-as-read'),
]