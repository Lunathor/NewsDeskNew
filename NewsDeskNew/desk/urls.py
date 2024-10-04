from django.urls import path, include
from .views import *

urlpatterns = [
    path('', PostListView.as_view(), name='MainPage'),
    path('post/<int:pk>/', post_review, name='PostReview'),
    path('post/create/', PostCreateView.as_view(), name='Create'),
    path('post/update/<int:pk>', PostUpdateView.as_view(), name='Update'),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name='Delete'),
    path('post/delete_image/<int:pk>', delete_image, name='delete_image'),
    path('post/delete_video/<int:pk>', delete_video(), name='delete_video'),
]
