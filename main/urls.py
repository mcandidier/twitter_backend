from django.urls import include, path
from rest_framework import routers
from .views import ProfileViewSet, TweetViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'tweets', TweetViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)), 
]