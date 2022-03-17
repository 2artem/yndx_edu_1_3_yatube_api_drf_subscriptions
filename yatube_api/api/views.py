from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import filters
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
from .permissions import IsOwnerOrReadOnly
from rest_framework import mixins


class CreateListViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """
    Кастомный базовый вьюсет:
    Создает объект (для обработки запросов POST) и
    возвращает список объектов (для обработки запросов GET).
    """
    pass


class PostViewSet(viewsets.ModelViewSet):
    """Предустановленный класс для работы с моделью Post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        """Переопределяем метод perform_create."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Предустановленный класс для работы с моделью Group."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(CreateListViewSet):
    """Предустановленный класс для работы с моделью Follow."""
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^following__username',)

    def get_queryset(self):
        """Изменяем базовый QuerySet, переопределив метод get_queryset."""
        new_qweryset = Follow.objects.filter(user=self.request.user)
        return new_qweryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Предустановленный класс для работы с моделью Comment."""
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)

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
