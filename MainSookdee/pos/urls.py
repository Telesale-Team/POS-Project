from django.urls import path
from .views import *
urlpatterns = [
    path('',POS,name='pos'),
    path('billing/', billing, name='billing'),
        
    path('billing/order', order, name='order'),
]