"""Представления API приложения posts."""
from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework import pagination

from api.permissions import AuthorOr401Permission
from api.serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)
from posts.models import Follow, Group, Post


class PostViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для обработки запросов по url('api/posts/').
    Обрабатывает url:
    ('api/posts/') - для получения списка объектов модели Post.
    ('api/posts/{post_id}) - для получения объекта модели Post по id.
    """
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, ]
    flterset_fields = ['author', 'pub_date', ]
    search_fields = ['text', ]
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        """Метод для получения набора объектов или объект по id."""
        if self.action == 'list':
            return Post.objects.all()
        post_id = self.kwargs.get('pk')
        return Post.objects.filter(id=post_id)

    def perform_create(self, serializer):
        """Метод для автоматического определения автора поста."""

        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет модели Group для реализации операций получения объектов."""
    serializer_class = GroupSerializer

    def get_queryset(self):
        if self.action == 'list':
            return Group.objects.all()
        group_id = self.kwargs.get('pk')
        return Group.objects.filter(id=group_id)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Comment для реализации всех возможных операций CRUD."""
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        if self.action == 'list':
            return post.comments.all()
        try:
            return post.comments.filter(pk=self.kwargs.get('pk'))
        except post.DoesNotExist:
            raise Http404('Такого комментария не существует.')

    def perform_create(self, serializer):
        """Метод для автоматической установки автора и поста комментария."""

        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(
            author=self.request.user,
            post=post,
        )


class FollowViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Follow для реализации POST и GET запросов."""
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['following__username', ]
    permission_classes = [AuthorOr401Permission, ]
    pagination_classes = None

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
