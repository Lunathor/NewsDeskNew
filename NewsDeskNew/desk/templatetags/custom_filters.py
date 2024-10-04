from django import template
from desk.models import *

register = template.Library()


@register.filter
def is_image_exist(value: Post) -> bool:
    if Image.objects.filter(post=value.pk).first():
        return True
    else:
        return False
    

@register.filter
def preview(value: Post) -> Image:
    image = Image.objects.filter(post=value).first()
    return image.file.url


@register.filter
def get_image(value: Post) -> list[Image]:
    return Image.objects.filter(post=value.pk).all()


@register.filter
def is_video_exist(value: Post) -> bool:
    if Video.objects.filter(post=value.pk).first():
        return True
    else:
        return False


@register.filter
def get_video(value: Post) -> list[Video]:
    return Video.objects.filter(post=value.pk).all()
