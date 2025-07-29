from django.urls import path
from .views import *
urlpatterns = [
    path('',POS,name='pos'),
    path('menu/', Menu, name='menu'),
    path('shop/', Shop, name='shop'),
    path('addshop/', AddShop, name='addshop'),
    path('view-data/<int:categoryid>', ViewData, name='view-data'),
    path('view-detail/<int:detialid>', DetailID, name='view-detail'),
    path('billing/', billing, name='billing'),        
    path('billing/order', order, name='order'),
    path('sell/', Admin_sell_product, name='admin_sell_product'),
]