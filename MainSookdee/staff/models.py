from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Permission_User (models.Model):
	name_permission = models.CharField(max_length=200)
	description_permission = models.TextField(null=True,blank=True)

		
	def __str__ (self):
		return str(self.name_permission)
	
class ProfileUser(models.Model):	 
	user = models.OneToOneField(User,on_delete=models.CASCADE) # ชื่อพนักงาน
	image_profile = models.ImageField('รูปภาพโปรไฟล์',upload_to='image_profile',null=True,blank=True,default='default.png')#รูปภาพโปรไฟล์
	address = models.CharField('ที่อยู่',max_length=255,blank=True,null=True)# ที่อยู่ 
	phone = models.CharField('เบอร์โทรศัพท์',max_length=10,blank=True) #  เบอร์โทรศัพท์
	#permission = models.ForeignKey(Permission_User,on_delete=models.CASCADE,verbose_name=("สิทธิ์การใช้งาน"))
	def __str__ (self):
		return str(self.user)
	
