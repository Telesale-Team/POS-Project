from django.urls import path
from . views import *
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', Account_Profile, name='profile'),
    path('register/', Register, name='register'),
    path('login/', User_login, name='login'),
    path('logout/', User_logout, name='logout'),
    path('forgot-password/', Forgot_Password, name='forgot-password'),
]
