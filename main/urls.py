from django.urls import include, path
from rest_framework import routers
from .views import ProfileViewSet, TweetViewSet, CommentViewSet, UserProfileViewSet

router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'tweets', TweetViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('users/<int:id>/', UserProfileViewSet.as_view({'get': 'retrieve', 'put': 'update_profile'})),
    path('accounts/profile/', UserProfileViewSet.as_view({'put': 'update_profile'})),
    path('', include(router.urls)), 
]