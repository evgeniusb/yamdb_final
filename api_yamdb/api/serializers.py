import re

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .validators import ValidateUsername


class UserSerializer(serializers.ModelSerializer, ValidateUsername):
    """Сериализатор для пользователей."""
    email = serializers.EmailField(
        max_length=300, required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email'),
                message='Нельзя повторно создать пользователя с таким же email'
            )
        ]

    def validate_email(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError(
                'Проверьте корректность ввода эл.почты!'
            )
        return value


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанра."""

    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории."""

    class Meta:
        model = Category
        exclude = ('id',)


class TitleListSerializer(serializers.ModelSerializer):
    """Сериализатор для Title только чтение"""
    category = CategorySerializer(many=False, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'genre', 'rating', 'category',
                  'name', 'description', 'year')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )
    year = models.PositiveIntegerField("Год выпуска", blank=True, null=True)

    def validate_year(self, value):
        year = timezone.now().year
        if not (value <= year):
            raise serializers.ValidationError(
                'Проверьте год выхода произведения!'
            )
        return value

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов о произведении."""
    author = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
    )
    title = serializers.SlugRelatedField(slug_field='name', read_only=True, )

    def validate_score(self, value):
        if not (1 <= value <= 10):
            raise serializers.ValidationError(
                'Оценка score должна быть в пределах от 1 до 10!'
            )
        return value

    def validate(self, data):

        request = self.context["request"]
        title_id = self.context["view"].kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if request.method == "POST":
            if Review.objects.filter(
                    title=title, author=request.user
            ).exists():
                raise ValidationError(
                    "Отзыв автора уже оставлен на данное произведение.")
        return data

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author', 'pub_date', )


class UserSignupSerializer(serializers.Serializer, ValidateUsername):
    email = serializers.EmailField(
        max_length=300, required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email'),
                message='Нельзя повторно создать пользователя с таким же email'
            )
        ]

    def create(self, validated_data):
        get_email = validated_data.get('email')
        user = User.objects.create(**validated_data)
        email = EmailMessage(
            'Confirmation_code',
            default_token_generator.make_token(user),
            to=[get_email]
        )
        email.send()
        return user


class TokenSerializer(serializers.Serializer):
    """Создаём сериализатор, наследник предустановленного класса Serializer"""
    username = serializers.CharField(max_length=256)
    confirmation_code = serializers.CharField(max_length=256)
