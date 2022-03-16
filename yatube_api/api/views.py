from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework import status
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from posts.models import Post
from posts.models import Group
from posts.models import Comment
from posts.models import Follow
from .serializers import PostSerializer
from .serializers import GroupSerializer
from .serializers import CommentSerializer
from .serializers import FollowSerializer
from rest_framework import permissions


class PostViewSet(viewsets.ModelViewSet):
    """Предустановленный класс для работы с моделью Post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Переопределяем метод perform_create."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Переопределяем метод perform_update."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        serializer.save(author=self.request.user, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """Переопределяем метод perform_destroy."""
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Предустановленный класс для работы с моделью Group."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(viewsets.ModelViewSet):
    """Предустановленный класс для работы с моделью Follow."""
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^following__username',)

    def get_queryset(self):
        """Изменяем базовый QuerySet, переопределив метод get_queryset."""
        new_qweryset = Follow.objects.filter(user=self.request.user)
        return new_qweryset

    def perform_update(self, serializer):
        """Переопределяем стандартный метод perform_update."""
        raise PermissionDenied('METHOD NOT ALLOWED')

    def perform_destroy(self, instance):
        """Переопределяем стандартный метод perform_destroy."""
        raise PermissionDenied('METHOD NOT ALLOWED')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Предустановленный класс для работы с моделью Comment."""
    serializer_class = CommentSerializer

    def perform_update(self, serializer):
        """Переопределяем стандартный метод perform_update."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        serializer.save(author=self.request.user, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """Переопределяем стандартный метод perform_destroy."""
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        """Переопределяем метод perform_create."""
        post_need_com = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(post=post_need_com, author=self.request.user)

    def get_queryset(self):
        """Изменяем базовый QuerySet, переопределив метод get_queryset."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        new_qweryset = Comment.objects.filter(post=post)
        return new_qweryset
