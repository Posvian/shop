from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username_validator = ASCIIUsernameValidator()

    username = models.CharField(
        verbose_name='username',
        max_length=150,
        unique=True,
        help_text='Допустимо использовать только латинские буквы. Длина не может превышать 150 символов',
        validators=[username_validator],
        error_messages={
            'unique': "Пользователь с таким логином уже существует."
        },
    )
    first_name = models.CharField(
        verbose_name='first_name',
        max_length=50,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='last_name',
        max_length=50,
        blank=True
    )
    age = models.PositiveIntegerField(
        verbose_name='age',
        blank=True,
        null=True
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=256,
        unique=True,
        error_messages={
            'unique': 'Пользователь с такой почтой уже зарегистрирован',
        },
    )
    is_staff = models.BooleanField(
        verbose_name='staff status',
        default=False,
        help_text='Пользователь с таким статусом может войти в раздел admin',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name
