from rest_framework import serializers
from django.db.models import Avg
from django.conf import settings

from reviews.models import (
    Review, Comment, Title, Category,
    Genre, YaMdbUser
)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для объекта класса Category."""
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для объекта класса Genre."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title при действии 'list', 'retrieve'."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        return Review.objects.filter(title=obj).aggregate(
            Avg('score')).get('score__avg')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для объекта класса Review."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('id', 'title', 'pub_date', 'author',)

    def validate(self, data):
        """
        Валидация на уже существующий отзыв к произведению от одного автора.
        """
        is_review_exist = Review.objects.filter(
            author=self.context['request'].user,
            title=self.context['view'].kwargs['title_id']
        ).exists()
        if self.context['request'].method == 'POST' and is_review_exist:
            raise serializers.ValidationError(
                'На одно произведение можно оставить только один отзыв!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для объекта класса Comment."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = serializers.PrimaryKeyRelatedField(
        read_only=True)
    review = serializers.PrimaryKeyRelatedField(
        read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


# Эндпоинт /singup/
class UserSingUpSerializer(serializers.ModelSerializer):
    """Сериализатор для объекта класса регистрации."""
    class Meta(object):
        model = YaMdbUser
        fields = ('email', 'username',)
        read_only_fields = ('role',)


# Эндпоинт /user/
class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для объекта класса user."""
    class Meta:
        model = YaMdbUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


# Эндпоинт /users/me/
class SelfUserPageSerializer(serializers.ModelSerializer):
    """Сериализатор своей страницы."""
    last_name = serializers.CharField(max_length=settings.MAX_LENGTH_USERNAME)

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = YaMdbUser
        read_only_fields = ('role',)


# Эндпоинт /token/
class TokenSerializer(serializers.Serializer):
    """Сериализатор получения токена."""
    username = serializers.CharField(max_length=settings.MAX_LENGTH_USERNAME)
    confirmation_code = serializers.CharField(
        max_length=settings.MAX_LENGTH_CODE
    )
