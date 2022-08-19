from django.contrib.auth.models import AbstractUser
from django.db import models


ADMIN = 'admin'
USER = 'user'


ROLE_CHOICES = [
    (ADMIN, ADMIN),
    (USER, USER),
]


class CustomUser(AbstractUser):
    username_validator = UsernameValidator()
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
        blank=False,
        null=False
    )
    email = models.EmailField(
        'e-mail',
        max_length=255,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN
