from django.urls import path
from .views import *

urlpatterns = [
    path('', Blogs, name='blogs'),
    path('menu/', Menu, name='menu'),
]
