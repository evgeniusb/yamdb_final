from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User
from .validators import year_validator


class Category(models.Model):
    """Модель для определения категории."""
    name = models.CharField(
        max_length=40,
        verbose_name='Категория'
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        unique=True
    )

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель для определения жанра."""
    name = models.CharField(max_length=150,
                            unique=True,
                            verbose_name='название жанра')
    slug = models.SlugField(max_length=50,
                            unique=True,
                            verbose_name='slug жанра')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=200
    )
    year = models.IntegerField(
        verbose_name='Год издания',
        validators=[year_validator],
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(verbose_name='Отзыв о произведении')
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        default=0,
        validators=[
            MaxValueValidator(10, message='Введите число не больше 10'),
            MinValueValidator(1, message='Введите число не меньше 1')],
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return self.text[:45] + ' ...'


class Comment(models.Model):
    text = models.TextField(verbose_name='Комментарий по отзыву')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE
    )
