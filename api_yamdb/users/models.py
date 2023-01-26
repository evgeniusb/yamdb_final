from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    ROLE_CHOISES = (
        (ADMIN, 'Администратор'),
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=30,
        null=True,
        blank=True,
        choices=ROLE_CHOISES,
        default=USER,
    )

    @property
    def is_administrator(self):
        return self.role == User.ADMIN

    @property
    def is_user(self):
        return self.role == User.USER

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR
