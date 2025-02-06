from django.urls import path
from .views import *
urlpatterns = [
    
    path('',Store, name='store'),
    path('create_product/',Add_Product, name='create-product'),
    path('view_product/<int:product_id>/',View_Product,name='view-product'),
    path('delete_product/<int:product_id>/',Delete_Product, name='delete-product'),
    path('edit_product/<int:product_id>/',Edit_Product, name='edit-product'),
    path('update_product/<int:product_id>/',Update_Product, name='update-product'),


    path('category_managment/',Category_managment, name='category-managment'),
    path('add_category/',Add_Category, name='add-category'),
    path('delete_category/<int:id>/',Delete_Category, name='delete-category'),
    path('edit_category/<int:id>/',Edit_Category, name='edit-category'),

    path('unit/',Unit_managment, name='unit'),
    path('edit_unit/<int:id>/',Edit_Unit,name='unit-edit'),
    path('delete_unit/<int:id>/',Delete_Unit,name='unit-delete'),
    path('update_unit/<int:id>/',Update_Unit,name='unit-update'),
    path('setting_general/',Setting,name='setting-general'),
]