from rest_framework import serializers
from django.contrib.auth.models import User

from posts.models import Post, Group, Comment, Follow


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, data):

        following_user = User.objects.filter(
            username=self.context['request'].data.get('following')).first()

        if 'following' not in self.context['request'].data:
            raise serializers.ValidationError(
                {'following': ['Обязательное поле.']}
            )

        if following_user == self.context['request'].user:
            raise serializers.ValidationError(
                {'following': ['Нельзя подписаться на самого себя!']})

        if Follow.objects.filter(user=self.context['request'].user,
                                 following=following_user).exists():
            raise serializers.ValidationError(
                {'following': ['Вы уже подписаны на этого пользователя.']}
            )

        return data


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'group', 'image')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'text', 'created')
        read_only_fields = ('post',)
