from django.shortcuts import render
from store.models import *
# Create your views here.
def Blogs(request):
	
	categorys = Category.objects.all()
	products = Product.objects.all()
	print(categorys)
	context = {
		"categorys": categorys,
		"products": products,
			}
	return render(request, 'blog/index.html',context)
