from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import pre_save
from django.dispatch import receiver
import re
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Создает и возвращает обычного пользователя с заданным именем пользователя и паролем.
        """

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Создает и возвращает суперпользователя с заданным именем пользователя и паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    telegram_username = models.CharField(max_length=500, blank=False,
                                         help_text="Юзернейм в телеграмме", unique=True)
    points_count = models.PositiveIntegerField(help_text="Количество очков", default=0)
    objects = CustomUserManager()
    tasks_count = models.PositiveIntegerField(help_text="Количество задач", default=0)

    def __str__(self):
        return self.telegram_username


def validate_telegram_username_format(value):
    # Проверка формата telegram_username с использованием регулярного выражения
    pattern = r'^@[\w]+$'
    if not re.match(pattern, value):
        raise ValidationError('Недопустимый формат telegram username. Используйте @ и буквы/цифры/подчеркивания.')


@receiver(pre_save, sender=User)
def validate_telegram_username(sender, instance, **kwargs):
    # Проверка, что telegram_username находится в списке разрешенных значений
    allowed_usernames = ["@username1", "@username2", "@username3"]  # Замените на свой список
    if instance.telegram_username not in allowed_usernames:
        raise ValueError(f"Недопустимый telegram username: {instance.telegram_username}. Регистрация запрещена.")

    validate_telegram_username_format(instance.telegram_username)
