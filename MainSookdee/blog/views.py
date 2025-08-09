from django.shortcuts import render
from store.models import *
# Create your views here.
def Blogs(request):
	
	categorys = Category.objects.all()
	products = Product.objects.all().order_by('-date_stamp')[:10]  # แสดงสินค้าล่าสุด 8 รายการ

	context = {
		"categorys": categorys,
		"products": products,
			}
	return render(request, 'blog/index.html',context)
