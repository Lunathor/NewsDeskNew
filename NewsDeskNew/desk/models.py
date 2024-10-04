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


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок поста')
    text = models.TextField(verbose_name='Содержание поста')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор поста')
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICE, verbose_name='Категория поста')
    datecreation = models.DateTimeField(auto_now_add=True)
    
    def preview(self):
        return self.text[0:123] + '...'
    
    def category_name(self):
        for category in CATEGORY_CHOICE:
            if self.category == category[0]:
                return category[1]
            
    def __str__(self):
        return f'{self.title.title()}'
    
    
class Image(models.Model):
    file = models.ImageField(upload_to='desk/gallery/images', verbose_name='Картинка')
    post = ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    
    
class Video(models.Model):
    url = EmbedVideoField(verbose_name="Ссылка на Видео")
    post = ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    text = models.TextField(verbose_name='Содержание комментария')
    datecreation = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False, verbose_name='Подтвержденный комментарий')
    
    def __str__(self):
        return f'{self.text}'
    
    
