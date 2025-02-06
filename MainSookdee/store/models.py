from django.db import models

# Create your models here.
from django.db import models
from staff.models import ProfileUser

class Category(models.Model):
    image_category = models.ImageField(upload_to='catagory_images/')
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=50)
    check_data = models.BooleanField(default=False,blank=True,null=True)
    date_stamp = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return self.name

class Product(models.Model):

    image = models.ImageField(upload_to='product_images/',default="image_product.jpg")#รูป
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)  #หมวดหมู่ การอ้างอิงถึง Category
    name = models.CharField(max_length=100,blank=True,null=True)#ชื่อภาษาไทย
    name_en = models.CharField(max_length=100,blank=True,null=True)#ชื่อภาษาอังกฤษ
    profit = models.CharField(max_length=100,blank=True,null=True)#คุณประโยชน์
    component = models.CharField(max_length=100,blank=True,null=True)#ส่วนประกอบ
    description = models.TextField(blank=True,null=True)#รายละเอียดอื่นๆ
    price = models.DecimalField(max_digits=10, decimal_places=2)#ราคา
    stock = models.BooleanField(default=True)#เช็คสต๊อก
    unit = models.ForeignKey(Unit, related_name='unit', on_delete=models.CASCADE)  #หน่วยนับ การอ้างอิงถึง Unit
    quatity = models.IntegerField(blank=True, null=True)#จำนวนสินค้า
    date_time = models.DateTimeField(auto_now_add=True,blank=True, null=True)#วันเวลา
    rate = models.IntegerField(blank=True, null=True,default=5)#ความนิยม
    

    def __str__(self):
        return self.name
    

class Order(models.Model):
    customer = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ])

    def __str__(self):
        return f"รหัสออร์เดอร์ {self.id} ลูกค้า {self.customer} { self.status} "

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"