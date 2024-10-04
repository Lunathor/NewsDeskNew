from django.urls import path, include
from .views import *


urlpatterns = [
    path('', PostListView.as_view(), name='MainPage'),
]