from django.urls import include, path, re_path
from rest_framework import routers
from .views import ProfileViewSet, TweetViewSet, CommentViewSet, UserProfileViewSet, UserUploadImageView

router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'tweets', TweetViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('users/<int:id>/', UserProfileViewSet.as_view({'get': 'retrieve'})),
    path('profile/', UserProfileViewSet.as_view({'put': 'update_profile'})),
    path('profile/image/', UserUploadImageView.as_view(), name='user-profile-image'),
    path('', include(router.urls)), 
]