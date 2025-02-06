from django.shortcuts import render,redirect,HttpResponse
from django.core.files.storage import FileSystemStorage
from . models import *
import os
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.

def Store (request):

	products = Product.objects.all()
	categorys = Category.objects.all()
	unit = Unit.objects.all()


	context = {"products":products,
			   "categorys":categorys,
			   "units":unit,}
	
	return render(request, 'store/store.html', context)
	#return render(request, 'store/general.html', context)

def Add_Product (request):

	products = Product.objects.all()
	category = Category.objects.all()
	unit = Unit.objects.all()

	if request.method == "POST" :

		data = request.POST.copy()

		image_data = request.FILES.get('productImages')
		description_data = data.get('inputDescription')
		inputcategory_data = data.get('inputCategory')
		name_product_th = data.get('inputNameth')
		name_product_en = data.get('inputNameen') #inputNameen
		price_data = data.get('inputPrice')
		quantity_data = data.get('inputQuantity')
		unit_data = data.get('inputUnit')
		component_data = data.get('inputComments')
		profit_data = data.get('inputProfit')
		rate_data = data.get('inputRate')
		stock_data = data.get('checkstock')

		## Test การทำงาน
		print(inputcategory_data)
		category_name = Category.objects.get(name=inputcategory_data)
		unit_name = Unit.objects.get(name=unit_data)

		# Save product in database
		Product.objects.create(
						image=image_data,#รูป
						category = category_name,#หมวดหมู่
						name=name_product_th,#ชื่อภาษาไทย
						name_en = name_product_en,#ชื่อภาษาอังกฤษ
						price=float(price_data),#ราคา
						stock=stock_data,#เช็คสต๊อก
						unit=unit_name,#หน่วยนับ
						quatity=int(quantity_data),#จำนวนสินค้า
						component = component_data,#ส่วนประกอบ
						profit = profit_data,#ประโยชน์
						description = description_data,#รายละเอียดอื่นๆ
						rate = rate_data,)
		
		messages.success(request,'บันทึกข้อมูลเรียบร้อยแล้ว')

		return redirect('store')  # หน้าแสดงรายการสินค้า

	context = {"products":products,
			   "categorys":category,
			   "units":unit,}
	
	return render(request, 'store/add-product.html', context)

def View_Product (request,product_id):
	product = Product.objects.get(pk=product_id)
	context = {"product":product,}
	return render(request, 'store/view_product.html', context)

def Delete_Product(request,product_id):
	Product.objects.get(pk=product_id).delete()
	return redirect('store')

def Edit_Product(request,product_id):

	product = Product.objects.get(id=product_id)
	category = Category.objects.all()
	unit = Unit.objects.all()

	if request.method == "POST":
		data = request.POST.copy()
		product = Product.objects.get(id=product_id)

		if product:

			category_data = Category.objects.get(name=data.get('inputCategory'))
			product.category = category_data
			product.name = data.get('inputNameth')
			product.name_en = data.get('inputNameen') #inputNameen
			product.price = data.get('inputPrice')
			product.quatity = data.get('inputQuantity')
			
			unit_data = Unit.objects.get(name = data.get('inputUnit'))
			product.unit = unit_data

			product.component = data.get('inputComments')			
			product.profit = data.get('inputProfit')
			#print(data)
			product.description = data['inputDescripstion']

			product.stock = data.get('checkstock')

			product.save()

			print("เซฟข้อมูลเรียบร้อยแล้ว",)
			return redirect('store')
	
	context = {"product":product,
			"categorys":category,
			"units":unit,}
	
	return render(request, 'store/edit-product.html', context)

def Update_Product(request,product_id):

	if request.method == "POST":
		data = request.POST.copy()
		product = Product.objects.get(id=product_id)

		image_data = request.FILES.get('productImages')
		description_data = data.get('inputDescription')
		inputcategory_data = data.get('inputCategory')
		name_product_th = data.get('inputNameth')
		name_product_en = data.get('inputNameen') #inputNameen
		price_data = data.get('inputPrice')
		quantity_data = data.get('inputQuantity')
		unit_data = data.get('inputUnit')
		component_data = data.get('inputComments')
		profit_data = data.get('inputProfit')
		description_data = data.get('')
		rate_data = data.get('inputRate')
		stock_data = data.get('checkstock')
		print(product.objects.all())

		print("component :",component_data)
		return redirect('store')

def Category_managment(request):

	category = Category.objects.all()
	context = {"category_data":category,}
	return render(request,'store/category-managment.html',context)

def Delete_Category(request,id):
	if request.method == "POST":
		category = Category.objects.get(id=id)
		print(category)
		category.delete()

	return redirect("category-managment")

def Edit_Category(request,id):

	if request.method == "POST":
		data = request.POST.copy()
		category = Category.objects.get(id=id)
		name = data['CategoryName']
		description = data['CategoryDescription']
		category.name = name
		category.description = description

		category.save()
		print("บันทึกข้อมูลเรียบร้อย")
		return redirect('category-managment')

def Add_Category(request):

	if request.method == "POST":
		data = request.POST.copy()
		
		image_data = request.FILES.get('CategoryImages')
		name = data['CategoryName']
		description_data = data['CategoryDescription']

		if Category.objects.filter(name=name).exists():
			print("มีหมวดหมู่นี้แล้ว")
		else:
			Category.objects.create(image_category=image_data,#รูป
							description = description_data,#รายละเอียดหมวดหมู่
							name=name,)#ชื่อหมวดหมู่
		
			messages.success(request,'บันทึกข้อมูลเรียบร้อยแล้ว')

		return redirect('category-managment')
	else:
		context = {}

		return render(request, 'store/category-managment.html', context)

def Unit_managment(request):

	unit_data = Unit.objects.all()		
	context = {'unit_data':unit_data,}
	return render(request,"store/unit.html",context)
	
def Edit_Unit(request,id):

	if request.method == "POST":
		unit_data = Unit.objects.get(id=id)
		unit_data.name = request.POST['edit-unit']
		#unit_data.save()
		return redirect('unit')

def Delete_Unit(request,id):

	if request.method == "POST":
		unit = Unit.objects.get(id=id)
		print(unit)
		unit.delete()
		return redirect('unit')

def Update_Unit(request,id):
	unit = Unit.objects.get(id=id)

	if request.method == "POST":
		data = request.POST.copy()
		checkData = data['check_unit']
		if checkData:
			unit.name = data['UnitName']
			unit.check_data = True
			unit.save()
			return redirect('unit')
		
		else:
			unit.name = data['UnitName']
			unit.check_data = False
			unit.save()
			return redirect('unit')
	else:
		return redirect('unit')	
	
def Setting (request):

	context = {}
	return render(request, 'store/setting-genaral.html', context)

