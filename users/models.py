from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    telegram_chat_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Telegram Chat ID',
        help_text='ID чата в Telegram для уведомлений'
    )
    timezone = models.CharField(
        max_length=50,
        default='Europe/Moscow',
        verbose_name='Часовой пояс'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
