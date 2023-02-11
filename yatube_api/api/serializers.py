from rest_framework import serializers

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post."""
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        required=False,
        allow_null=True,
        default=None,
    )
    author = serializers.StringRelatedField(
        read_only=True,
    )

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['post', ]


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""
    description = serializers.CharField(required=False)

    class Meta:
        model = Group
        fields = '__all__'

    def validate_slug(self, value):
        """Метод для проверки уникальости slug-поля группы."""
        if User.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                'Группа с таким slug-полем уже существует.',
            )
        return value


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow."""
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, data):
        if self.context['request'].user != data['following']:
            return data
        raise serializers.ValidationError('Вы не можете подписаться на себя.')

    validators = [
        serializers.UniqueTogetherValidator(
            queryset=Follow.objects.all(),
            fields=['user', 'following'],
        )
    ]
