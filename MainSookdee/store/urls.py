from django.urls import path
from .views import *
urlpatterns = [
    
    path('',Product_Managment, name='product-managment'),
    path('create_product/',Create_Product, name='create-product'),
    path('view_product/<int:product_id>/',View_Product,name='view-product'),
    path('delete_product/<int:product_id>/',Delete_Product, name='delete-product'),
    path('edit_product/<int:product_id>/',Edit_Product, name='edit-product'),
    path('update_product/<int:product_id>/',Update_Product, name='update-product'),
    path('update-image-order//',Update_Image_Order,name='update_image_order'),

    path('category_managment/',Category_managment, name='category-managment'),
    path('create_category/',Create_Category, name='create-category'),
    path('view_category/<int:category_id>/',View_Category, name='view-category'),
    path('delete_category/<int:category_id>/',Delete_Category, name='delete-category'),
    path('edit_category/<int:category_id>/',Edit_Category, name='edit-category'),

    path('unit_managment/',Unit_managment, name='unit-managment'),
    path('create_unit/',Create_Unit, name='create-unit'),
    path('view_unit/<int:unit_id>/',View_Unit,name='view-unit'),
    path('edit_unit/<int:unit_id>/',Edit_Unit,name='edit-unit'),
    path('delete_unit/<int:unit_id>/',Delete_Unit,name='delete-unit'),

    path('setting_general/',Setting,name='setting-general'),
]