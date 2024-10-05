import pyotp
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.reverse import reverse_lazy
from .models import User, Post


def conf_code_generator(user: User) -> str:
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
    user.email_conf_code = totp.now()
    user.save()
    
    return totp.now()


def conf_code_verificator(code: str, user: User) -> bool:
    return code == user.email_conf_code


def confirmation_code_sender(user: User) -> None:
    email = user.email
    email_conf_code = user.email_conf_code
    
    send_mail(
        'Подтверждение регистрации',
        f'Ваш одноразовый код для подтверждения регистрации на сайте: {email_conf_code}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
   
    
def email_about_new_comment(author: User, post_pk: int) -> None:
    email = author.email
    url = reverse_lazy('PersonalCabinet')
    post = Post.objects.get(pk=post_pk)
    msg_title_of_post = post.preview()
    
    send_mail(
        'Новый комментарий',
        f'''Ваш пост {msg_title_of_post}, прокомментировали.
        Для того чтобы комментарий отобразился под постом утвердите его в личном кабинете: {url}''',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    
    
def postman(msg_title_of_post: str, msg_text_of_post: str) -> None:
    for user in User.objects.filter(about_sub=True):
        email = user.email
        
        send_mail(
            msg_title_of_post,
            msg_text_of_post,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )
