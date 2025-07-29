from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.core.files.storage import FileSystemStorage
from . models import *
import os
from django.http import JsonResponse
from django.contrib import messages
import time
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from pathlib import Path
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
BASE_DIR = Path(__file__).resolve().parent.parent

#Product Manament Functions
@csrf_exempt
def Update_Image_Order(request):
	if request.method == "POST":		
		data = json.loads(request.POST.get("ordered_ids"))
		for index, image_id in enumerate(data):
			ProductImage.objects.filter(id=image_id).update(order=index)
		return JsonResponse({"status": "success"})
	return JsonResponse({"status": "failed"}, status=400)

def Product_Managment (request):

	products = Product.objects.all()
	categorys = Category.objects.all()
	unit = Unit.objects.all()


	if request.method == "POST" :		
		data = request.POST.copy()		
		#เมื่อจะทำการบันทึกข้อมูล ให้เช็คข้อมูลในระบบว่ามีข้อมูลนี้ใหม?
		product_name = Product.objects.filter(name=data.get('name')).exists()

		if product_name:
			#ถ้ามีข้อมูลนี้ในระบบ ให้ดึงข้อมูลออกมา
			product_id = Product.objects.filter(id=data.get('product_id')).first()			
			product_id.name = data.get('name')
			product_id.description = data.get('description')
			product_id.image_product = request.FILES.get('image')
			product_id.category = Category.objects.filter(name = data.get('category')).first()
			product_id.price = data.get('price')
			product_id.cost = data.get('saleprice')
			product_id.stock_quantity = data.get('stock_quantity')
			product_id.reorder_level = data.get('reorder_level')
			product_id.supplier = Supplier.objects.filter(name=data.get('supplier')).first()
			product_id.unit = Unit.objects.filter(name=data.get('unit')).first()

			if data.get('check_data') == 'on':
				product_id.check_data = True
				product_id.save()
				messages.success(request,'บันทึกข้อมูลเรียบร้อยแล้ว')

				# หลังจาก save แล้วให้ทำการทำตามคำสั่งปุ่มกดที่ส่งมาให้ return redirect ไปที่ไหน
				if 'save' in request.POST:
					return redirect('product-managment')
				
				elif 'save-addNew' in request.POST:

					return redirect('create-product')
				
				elif 'save-edit' in request.POST:					
					product_id = Product.objects.get(id=data.get('product_id'))	
					#print(data)
					return redirect('edit-product',product_id)
				else:
					return redirect('create-product')
				
			else:
				product.check_data = False
				product.save()

				if 'save' in request.POST:
					return redirect('product-managment')
				else:
					return redirect('create-product')

			
		else:
			#ถ้าไม่มีข้อมูลให้บันทึกข้อมูลใหม่
			product = Product()				
			product.name = data.get('name')
			product.description = data.get('description')
			product.image_product = request.FILES.get('image')
			product.category = Category.objects.get(id=int(data.get('category')))
			product.price = data.get('price')
			product.cost = data.get('saleprice')
			product.stock_quantity = data.get('stock_quantity')
			product.reorder_level = data.get('reorder_level')
			product.supplier =Supplier.objects.get(id=int(data.get('supplier')))
			product.unit = Unit.objects.get(id =int(data.get('unit')))

			if data.get('check_data') == 'on':
				product.check_data = True
				product.save()

				# หลังจาก save แล้วให้ทำการทำตามคำสั่งปุ่มกดที่ส่งมาให้ return redirect ไปที่ไหน
				if 'save' in request.POST:
					return redirect('product-managment')
				elif 'save-addNew' in request.POST:
					return redirect('create-product')
				
				elif 'save-edit' in request.POST:					
					product_id = Product.objects.get(id=data.get('product_id'))	
					#print(data)			
					return redirect('edit-product',product_id)
				else:
					return redirect('create-product')
			else:
				product.check_data = False
				product.save()

				if 'save' in request.POST:
					return redirect('product-managment')
				else:
					return redirect('create-product')
				

	context = {"products":products,
			   "categorys":categorys,
			   "units":unit,}
	
	return render(request, 'store/product-managment.html', context)


def View_Product (request,product_id):
	product_id = Product.objects.get(pk=product_id)
	categorys = Category.objects.all()
	units = Unit.objects.all()
	suppliers = Supplier.objects.all()

	context = {"product":product_id,
			"categorys":categorys,
			"units":units,
			"suppliers":suppliers,

			}
	return render(request, 'store/view_product.html', context)

def Delete_Product(request,product_id):
	Product.objects.get(pk=product_id).delete()	
	messages.success(request,'ลบข้อมูลเรียบร้อยแล้ว')
	return redirect('category-managment')

def Edit_Product(request,product_id):

	product = Product.objects.get(pk=product_id)	
	category = Category.objects.all()
	
	context = {"product":product,
			   "category":category,}
	
	return render(request, 'store/edit-productV2.html', context)

def Update_Product(request,product_id):

	if request.method == "POST":
		data = request.POST.copy()
		product = Product.objects.get(pk=product_id)
		category = Category.objects.get(name=data.get('category'))
		unit = Unit.objects.get(name=data.get('unit'))

		if product:
			product.name = data.get('name_th')
			product.name_en = data.get('name_en')
			product.profit = data.get('profit')
			product.component = data.get('component')
			product.description = data.get('description')
			product.price = data.get('price')
			product.stock = data.get('radio') == "on"
			product.quatity = data.get('quantity')
			product.category = category	
			product.rate = data.get('rate')		
			product.unit = unit #Unit.objects.get(pk=data.get('unit'))
			product.save()
			return redirect('product-managment')
		else:
			print("ไม่พบข้อมูล")
			return redirect('product-managment')
	print("NO Sumit Post")
	return redirect ('product-managment')

def Create_Product (request):

	categorys = Category.objects.all()
	units = Unit.objects.all()
	products = Product.objects.all()
	suppliers = Supplier.objects.all()

	if request.method == "POST":

		data = request.POST.copy()

		data_name = data['name']
		data_category = data['category']
		data_image = request.FILES.get('image')
		data_detial = data['description']
		data_supplier = data['supplier']
		data_price = data['price']
		data_saleprice = data['saleprice']
		data_stock_quantity = data['stock_quantity']
		data_unit = data['unit']
		data_reorder_level = data['reorder_level']
		data_checkData = data['check_data']
		print('data_category',data_category)
		print('data_supplier',data_supplier)
		print('data_checkData',data_checkData)
		print('data_unit',data_unit)
		newProduct=Product.objects.update_or_create(
			name=data_name,
			defaults={
				'name':data_name,
				'category':Category.objects.get(id=data_category),
			 	'image_product':data_image,
			 	'description':data_detial,
			 	'supplier':Supplier.objects.get(id=data_supplier),
			 	'price':data_price,
				'cost':data_saleprice,
			 	'stock_quantity':data_stock_quantity,
			 	'unit':Unit.objects.get(id=data_unit),
			 	'reorder_level':data_reorder_level if data_reorder_level else 0,
			 	'check_data':data_checkData
				 
				})
		messages.success(request,f'บันทึกข้อมูล { data_name } เรียบร้อยแล้ว')
		newProduct = Product.objects.filter(name=data_name).first()
		if 'save' in request.POST:
			return redirect('product-managment')
		elif 'save-add' in request.POST:
			return redirect('create-product')
		elif 'save-edit' in request.POST:
			return redirect('view-product',newProduct.id)
		else:
			return redirect('product-managment')



	context = {
		"categorys":categorys,
		"units":units,
		"products":products,
		"suppliers":suppliers,
	}
	return render(request, 'store/add-product.html',context)

def Delete_Product(request,product_id):
	product = Product.objects.get(id=product_id)
	product.delete()
	messages.error(request,f'ลบข้อมูล { product.name } เรียบร้อยแล้ว')
	return redirect('product-managment')


#Category Manament Functions
def Category_managment(request):

	category = Category.objects.all()

	if request.method == 'POST':
		cat_code = request.POST.get('category_code')		
		name = request.POST.get('name-category')
		description = request.POST.get('description')
		check_data = request.POST.get('check_data')
		image = request.FILES.get('image')

		category = Category.objects.get(pk=cat_code)

		if category:
			#print('มีข้อมูลนี้ในระบบแล้ว')
			if 'save' in request.POST:
				# บันทึก/สร้างใหม่
				print("กำลังทำการ [Save]")
				category.name = name
				category.description = description
				category.check_data = check_data if check_data else category.check_data
				category.image_category = image if image else category.image_category
				category.save()


				return redirect('category-managment')  # เปลี่ยนเป็น URL ของหน้ารายการหมวดหมู่

			elif 'save-edit' in request.POST:
				# บันทึก/แก้ไข
				category.name = name
				category.description = description
				category.check_data = check_data if check_data else category.check_data
				category.image_category = image if image else category.image_category
				category.save()

				#messages.warning(request,f'แก้ไขข้อมูล { cat } เรียบร้อยแล้ว')
				return redirect('view-category',cat_code)  # เปลี่ยนเป็น URL ของหน้ารายการหมวดหมู่
			
			elif 'save-add' in request.POST:
				# บันทึก/สร้างใหม่ (เคลียร์ค่า category_id เพื่อสร้างใหม่)
				category.name = name
				category.description = description
				category.check_data = check_data if check_data else category.check_data
				category.image_category = image if image else category.image_category
				category.save()

				return redirect('create_category')

			elif 'delete' in request.POST:
				# ลบข้อมูล
				category.delete()
				return redirect('category-managment')
		
		else :
			#print('ไม่มีข้อมูลนี้ในระบบ')
			if 'save' in request.POST:
				# บันทึก/สร้างใหม่
				category = Category()
				category.name = name
				category.description = description
				category.check_data = check_data
				category.image_category = image
				category.save()

				return redirect('category-managment')  # เปลี่ยนเป็น URL ของหน้ารายการหมวดหมู่
			elif 'save-add' in request.POST:
				# บันทึก/สร้างใหม่ (เคลียร์ค่า category_id เพื่อสร้างใหม่)
				category = Category()
				category.name = name
				category.description = description
				category.check_data = check_data
				category.image_category = image
				category.save()			

				return redirect('create-category')
			elif 'save-edit' in request.POST:

				# บันทึก/แก้ไข
				category = Category()
				category.name = name
				category.description = description
				category.check_data = check_data
				category.image_category = image
				category.save()

				return redirect('view-category',category.id)  # เปลี่ยนเป็น URL ของหน้ารายการหมวดหมู่
			else:

				return redirect('category-managment')

	context = {"category":category,}
	return render(request,'store/category-managment.html',context)

def Create_Category(request):

	category_data = Category.objects.all()

	if request.method == "POST":
		data = request.POST.copy()
		name = data.get('name-category')
		description = data.get('description')
		#check_data = data.get('check_data')
		
		if 'image' in request.FILES:
			image = request.FILES.get('image')
			Category.objects.update_or_create(name=name,defaults={'description':description,'image_category':image})
		
			if 'save' in request.POST:
				return redirect('category-managment')
		
		else:
			Category.objects.update_or_create(name=name,defaults={'description':data['description'],'image_category':'category_images/images.png'})
		messages.success(request,f'บันทึกข้อมูล { name } เรียบร้อยแล้ว')
		return redirect('category-managment')



	context = {'category_data':category_data,}
	return render(request, 'store/add-category.html', context)

def View_Category(request,category_id):
	category_id = Category.objects.get(id=category_id)
	products = Product.objects.filter(category=category_id)
	
	context = {"category_id":category_id,
			"products":products,}
	return render(request, 'store/view-category.html', context)

def Edit_Category(request,categoryID):

	if request.method == "POST":		
		data = request.POST.copy()
		category = Category.objects.get(id=categoryID)
		category.description = data['inputDescription']
		category.name = data['name-category']
		category.save()
		messages.warning(request,f'แก้ไขข้อมูล { category.name } เรียบร้อยแล้ว')
		return redirect('category-managment')

def Delete_Category(request,category_id):
	category = Category.objects.get(id=category_id)
	category.delete()
	messages.error(request,f'ลบข้อมูล { category.name } เรียบร้อยแล้ว')
	print('ลบข้อมูลเรียบร้อยแล้ว')
	return redirect('category-managment')


#Unit Manament Functions
def Unit_managment(request):

	unit_data = Unit.objects.all()

	if request.method == "POST":
		data = request.POST.copy()
		name = data['name']
		check_data = Unit.objects.filter(name=name)
		
		if check_data.exists():
			print('มีข้อมูลนี้ในระบบแล้ว')
			print(data)
			if 'save' in request.POST:
				messages.warning(request,f'ข้อมูล { name } ตรวจสอบพบมีข้อมูลนี้ในระบบแล้ว กรุณาเปลี่ยนชื่อใหม่อีกครั้ง')
				return redirect('unit-managment')

			elif 'save-edit' in request.POST:
				messages.warning(request,f'มีข้อมูล { name } ตรวจสอบพบมีข้อมูลนี้ในระบบแล้ว กรุณาเปลี่ยนชื่อใหม่อีกครั้ง')
				unit_id = check_data.first().id
				return redirect('view-unit',unit_id)
			
			if 'save-add' in request.POST:
				messages.warning(request,f'มีข้อมูล { name } ตรวจสอบพบมีข้อมูลนี้ในระบบแล้ว กรุณาเปลี่ยนชื่อใหม่อีกครั้ง')
				return redirect('create-unit')
			
		else:
			print('ไม่มีข้อมูลนี้ในระบบ')
			unit = Unit()
			unit.name = name
			unit.save()
			messages.success(request,f'บันทึกข้อมูล { unit.name } เรียบร้อยแล้ว')
			if 'save' in request.POST:
				return redirect('unit-managment')
			elif 'save-add' in request.POST:
				return redirect('create-unit')
			elif 'save-edit' in request.POST:
				return redirect('edit-unit',unit.id)
			else:
				return redirect('unit-managment')	

	context = {'unit_data':unit_data,}
	return render(request,"store/unit-managment.html",context)

def Create_Unit(request):
	unit_data = Unit.objects.all()
	context = {'unit_data':unit_data,}
	return render(request,"store/add-unit.html",context)

def Edit_Unit(request,unit_id):
	unit_data = Unit.objects.get(id=unit_id)
	context = {'unit_data':unit_data,}
	return render(request, 'store/view-unit.html',context)
	
def Delete_Unit(request,unit_id):
	unit = Unit.objects.get(id=unit_id)
	unit.delete()
	messages.error(request,f'ลบข้อมูล { unit.name } เรียบร้อยแล้ว')
	return redirect('unit-managment')

def View_Unit(request,unit_id):
	unit = Unit.objects.get(id=unit_id)
	context = {'unit':unit,}
	return render(request, 'store/view-unit.html',context)
	
def Setting (request):

	context = {}
	return render(request, 'store/setting-genaral.html', context)

