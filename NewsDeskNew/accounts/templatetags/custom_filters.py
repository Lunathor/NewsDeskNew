from django import template
from desk.models import Comment

register = template.Library()


def is_comments_exist(pk:int) -> bool:
    if Comment.objects.filter(post=pk, is_confirmed=False).exists():
        return True
    else:
        return False
    