from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import ForeignKey
from embed_video.fields import EmbedVideoField

# Create your models here.

CATEGORY_CHOICE = [
    ("TA", "Танки"),
    ("HE", "Хилы"),
    ("DD", "ДД"),
    ("TR", "Торговцы"),
    ("GM", "Гильдмастеры"),
    ("QG", "Квестгиверы"),
    ("BS", "Кузнецы"),
    ("SK", "Кожевники"),
    ("AL", "Зельевары"),
    ("SM", "Мастера заклинаний"),
]


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    email_conf_code = models.CharField(max_length=6, blank=True, null=True)
    users_comments = models.BooleanField(default=True, verbose_name="Новые комментарии")
    about_sub = models.BooleanField(default=False, verbose_name="Новости сайта")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f'{self.username}'
    
