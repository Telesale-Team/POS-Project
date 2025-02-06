from django.urls import path
from . views import *

urlpatterns = [
    path('',invoice_dashboard, name='invoice_dashboard'),
    path('customer/',customer_invoice, name='customer_invoice')
]