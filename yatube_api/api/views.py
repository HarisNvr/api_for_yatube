from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, filters, mixins
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .serializers import (
    FollowSerializer, PostSerializer, GroupSerializer, CommentSerializer
)
from posts.models import Post, Group, Comment, Follow
from .permissions import IsAuthorOrReadOnlyPermission

User = get_user_model()


class CreateListViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pass


class FollowViewSet(CreateListViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def create(self, request, *args, **kwargs):
        data = request.data
        following_username = data.get('following')
        following_user = User.objects.filter(
            username=following_username
        ).first()

        if not following_username:
            raise ValidationError({'following': ['Обязательное поле.']})

        if not following_user:
            raise ValidationError(
                {'following': ['Такого пользователя не существует.']}
            )

        if request.user == following_user:
            raise ValidationError(
                {'following': ['Нельзя подписаться на самого себя!.']}
            )

        if request.user.followings.filter(following_id=following_user.id):
            raise ValidationError(
                {'following': ['Вы уже подписаны на этого пользователя.']}
            )

        follow_instance = Follow.objects.create(
            user=request.user,
            following=following_user
        )

        serializer = self.get_serializer(follow_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = self.request.user.followings.all()
        return queryset


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        post = self.get_post()
        return post.comments.all()

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_destroy(instance)

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)
