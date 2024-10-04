from django.contrib import admin
from multiprocessing.reduction import register
from .models import *


# Register your models here.


class ImageLine(admin.TabularInline):
    model = Image
    extra = 1
    max_num = 5


class VideoLine(admin.TabularInline):
    model = Video
    extra = 1
    max_num = 2


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('pk', 'title', 'text', 'author', 'category')
    inlines = [ImageLine, VideoLine]


class ImageAdmin(admin.ModelAdmin):
    model = Image
    list_display = ('pk', 'file')
    
    
admin.site.register(Post, PostAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(User)
