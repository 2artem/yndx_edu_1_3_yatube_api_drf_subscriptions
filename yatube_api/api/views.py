from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from posts.models import Post
from posts.models import Group
from posts.models import Comment
from posts.models import Follow
from .serializers import PostSerializer
from .serializers import GroupSerializer
from .serializers import CommentSerializer
from .serializers import FollowSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Предустановленный класс для работы с моделью Post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer

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
        #  Переопределяем стандартный метод
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Предустановленный класс для работы с моделью Group."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(viewsets.ReadOnlyModelViewSet):#вопрос по вью
    """Предустановленный класс для работы с моделью Follow."""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


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
        #  Переопределяем стандартный метод
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
