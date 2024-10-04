from django import template
from desk.models import *

register = template.Library


@register.filter
def is_image_exist(value: Post) -> bool:
    if Image.objects.filter(post=value.pk).first():
        return True
    else:
        return False
    
    
def preview(value: Post) -> Image:
    image = Image.objects.filter(post=value).first()
    return image.file.url
