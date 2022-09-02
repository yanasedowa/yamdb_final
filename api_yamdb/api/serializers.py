from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.db.models import Avg
from reviews.models import (
    Category, Comment, Genre, Review, Title, User,
)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'category', 'genre'
        )
        model = Title


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'category', 'genre'
        )
        model = Title

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score'))
        if rating['score__avg']:
            return int(rating['score__avg'])
        return None


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, date):
        method = self.context['request'].method
        if method == 'POST':
            author = self.context['request'].user
            title = self.context['view'].kwargs.get('title_id')
            if not author.is_authenticated:
                return date
            if author.reviewer.filter(title=title).exists():
                raise ValidationError(
                    f'Пользователь {author} может оставить'
                    f' один отзыв на произведение {title}'
                )
        return date


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
