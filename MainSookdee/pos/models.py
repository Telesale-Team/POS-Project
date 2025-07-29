from django.db import models
from store.models import Product
from staff.models import Customer
from django.contrib.auth.models import User

# -----------------------------
# Model สำหรับออเดอร์และรายการสินค้าในออเดอร์
# -----------------------------
class Order(models.Model):
    STATUS_CHOICES = (
        ('waiting', 'รอ Admin รับออร์เดอร์'),
        ('accepted', 'รับออร์เดอร์'),
        ('shipping', 'จัดส่ง'),
        ('delivered', 'จัดส่งเรียบร้อย'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.customer)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # ราคาต่อชิ้น ณ เวลาที่สั่งซื้อ
    
    def __str__(self):
        return self.product.name

# -----------------------------
# Model สำหรับบันทึกการเปลี่ยนแปลง (Log)
# -----------------------------
class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Log: {self.action} at {self.created_at}"
