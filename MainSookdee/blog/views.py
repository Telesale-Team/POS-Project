from django.shortcuts import render
from store.models import *
# Create your views here.
def Blogs(request):
	context = {}
	return render(request, 'blog/index.html',context)


def Menu (request):
    categories = Category.objects.all()
    menu_items = Product.objects.all()
    return render(request, 'blog/menu.html', {'categories': categories, 'menu_items': menu_items})