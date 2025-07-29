from django.db import models
from staff.models import ProfileUser
from django.contrib.auth.models import User
from django.db import models

class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    image_category = models.ImageField(upload_to='category_images/', default='category_images/images.png')
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True)
    check_data = models.BooleanField(default=False)  # ตั้งค่า default เป็น False เพื่อให้สอดคล้องกัน

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "หมวดหมู่สินค้า"
        verbose_name_plural = "หมวดหมู่สินค้า"

class CategoryImage(models.Model):
    category = models.ForeignKey(Category, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='category_images/')

    def __str__(self):
        return f"Image for {self.category.name}"

class Unit(models.Model):
    name = models.CharField(max_length=50, unique=True)  # ป้องกันชื่อหน่วยซ้ำกัน
    check_data = models.BooleanField(default=False)
    date_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "หน่วยสินค้า"
        verbose_name_plural = "หน่วยสินค้า"

class Product(models.Model):
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image_product = models.ImageField(upload_to='product_images/',default='product_images/image_product.jpg')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_quantity = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=0)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name='products')
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True,default='ชิ้น')
    check_data = models.BooleanField(default=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "สินค้า"
        verbose_name_plural = "สินค้า"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    is_primary = models.BooleanField(default=False)  # ใช้กำหนดรูปหลักของสินค้า
    order = models.PositiveIntegerField(default=0)  # ฟิลด์จัดลำดับภาพ
    uploaded_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.product.name} - {self.caption or 'Image'}"

    class Meta:
        ordering = ['order']  # ให้เรียงตามค่า order
        verbose_name = "รูปภาพสินค้า"
        verbose_name_plural = "รูปภาพสินค้า"

class StockInventory(models.Model):

    CHANGE_TYPE_CHOICES = (
        ('restock', 'Restock'),
        ('shop', 'shop'),
        ('sale','Sale'),
        ('out', 'out'),
        ('return', 'Return'),
        ('instock', 'instock'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=20, choices=CHANGE_TYPE_CHOICES)
    quantity = models.IntegerField()
    movement_date = models.DateTimeField(auto_now_add=True)
    reference_number = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stock_movements')

    def __str__(self):
        return f"{self.movement_type} - {self.product.name} ({self.quantity})"

class Inventory(models.Model):

    CHANGE_TYPE_CHOICES = (
        ('restock', 'Restock'),
        ('sale','Sale'),
        ('out', 'out'),
        ('return', 'Return'),
        ('instock', 'instock'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_logs')
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPE_CHOICES)
    quantity = models.IntegerField()  # จำนวนที่เปลี่ยนแปลง (สามารถเป็นค่าลบได้ในบางกรณี)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.change_type} - {self.product.name}"
