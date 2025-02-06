from django.urls import path
from . views import *
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', Account_Profile, name='profile'),
    path('register/', Register, name='register'),
    path('logout/',user_logout, name='logout'),
    path('login/',auth_views.LoginView.as_view(template_name="account/login.html"),name="login"),
    path('forgot-password/',Forgot_Password, name='forgot-password'),

]
