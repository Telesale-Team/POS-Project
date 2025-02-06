from django.db import models

class Category(models.Model):
    image_category = models.ImageField(upload_to='catagory_images/')
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name