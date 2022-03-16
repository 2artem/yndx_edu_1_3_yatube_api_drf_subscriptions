from django.urls import path
from django.urls import include
from rest_framework.routers import SimpleRouter
from api.views import PostViewSet
from api.views import GroupViewSet
from api.views import CommentViewSet
from api.views import FollowViewSet

router = SimpleRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
router.register('follow', FollowViewSet, basename='follower')
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
