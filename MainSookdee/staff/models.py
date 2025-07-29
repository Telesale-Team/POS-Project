from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# Create your models here.


class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image_profile = models.ImageField('รูปภาพโปรไฟล์', upload_to='image_profile', null=True, blank=True, default='default.png')
    address = models.CharField('ที่อยู่', max_length=255, blank=True, null=True)
    phone = models.CharField('เบอร์โทรศัพท์', max_length=10, blank=True)
    # หากต้องการกำหนดสิทธิ์ให้ uncomment ฟิลด์ด้านล่าง:
    # permission = models.ForeignKey(Permission_User, on_delete=models.CASCADE, verbose_name="สิทธิ์การใช้งาน", null=True, blank=True)

    def __str__(self):
        return str(self.user)

# -----------------------------
# Model สำหรับลูกค้าสมัครสมาชิก (Customer)
# -----------------------------

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user)
    