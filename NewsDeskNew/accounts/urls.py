from django.urls import path, include
from .views import *


urlpatterns = [
    path('signup/', SignUp, name='SignUp'),
    path('verification/<int:user_id>', Verification, name='Verification'),
    path('personalcabinet/', PersonalCabinetView, name='PersonalCabinet'),
    path('user/', include('django.contrib.auth.urls')),
    path('user/logout/', Logout, name='Logout'),
]