# Create your models here.
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

NULLABLE = {'blank': True, 'null': True}


# class CustomUserManager(UserManager):
#     def _create_user(self, email, password, **extra_fields):
#         email = self.normalize_email(email)
#         user = self.model(email=email,
#                           is_active=True,
#                           **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, email=None, password=None, **extra_fields):
#         return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    модель пользователя
    """
    username = None
    email = models.EmailField(verbose_name='почта', unique=True)
    tg_username = models.CharField(max_length=32, verbose_name='логин в Телеграме', **NULLABLE)
    chat_id = models.CharField(max_length=50, verbose_name='идентификатор чата', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
