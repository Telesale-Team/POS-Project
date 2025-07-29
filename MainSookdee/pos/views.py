from django.shortcuts import render,redirect,HttpResponse
import json
from . models import Order,OrderItem,Log
from store.models import *
from django.utils import timezone
from django.contrib import messages


def create_log(user, action):
	from .models import Log  # import ภายในฟังก์ชันเพื่อหลีกเลี่ยงปัญหา circular imports
	Log.objects.create(user=user, action=action)


def Shop (request):
	products = Product.objects.filter(check_data=True)
	context = {
		"products":products,
	}
	return render(request, 'pos/shop.html', context)
	
def AddShop(request):
	products =	Product.objects.all()
	context = {
		"products":products,
	}
	return render(request, 'pos/addshop.html', context)

def POS (request):

	products = Product.objects.all()
	image_product = ProductImage.objects.all()
	
	context = {
		"products":products,
		"image_product":image_product,
	}
	return render(request, 'pos/pos.html', context)

def dashboard(request):
	return render(request, 'dashboard.html')

def Menu (request):

	stock_product = StockInventory.objects.all()
	categorys = Category.objects.filter(check_data = True)
	products = Product.objects.all()


	context = {
		"stock_product": stock_product,
		"categorys":categorys,
		"products":products,

	}
	return render(request, 'pos/MenuV3.html', context)
	#return render(request, 'base/pos/base-pos.html', context)

def ViewData (request,categoryid):
	products = Product.objects.filter(category=categoryid)
	category_name = Category.objects.get(id=categoryid)
	context = {
		"products": products,
		"category_name": category_name,
	}
	return render(request, 'pos/view-data.html', context)

def DetailID (request,detialid):
	products = Product.objects.filter(id=detialid)
	context = {

		"product": products,
	}
	return render(request, 'pos/view-detail.html', context)

def billing(request):

	print("Test")
	if request.method == 'GET':
		return render(request, 'pos/billing.html')
	
	else:
		cid = request.POST.get('customerID', None)
		customer = Customer.objects.get(pk=cid)
		products = list(Product.objects.all())
		# context = { 'cust' : customer.identity,
		#             'name' : customer.name,
		#             'balance' : customer.balance,
		#             'products': products, }

		return render(request, 'pos/billing_details.html', {'customer': customer, 'products': products})

def order(request):
	if request.method == 'POST':
		data = json.loads(request.POST.get('data', None))
		if data is None:
			raise AttributeError
		print(data)
		customer = Customer.objects.get(pk=data['customer_id'])
		order = Order.objects.create(customer=customer,
									total_price=data['total_price'],
									success=False)
		for product_id in data['product_ids']:
			OrderItem(product=Product.objects.get(pk=product_id), order=order).save()
		if data['total_price'] <= customer.balance:
			customer.balance -= int(data['total_price'])
			customer.save()
			order.success = True
		order.save()
		return render(request, 'pos/order.html', {'success' : order.success})
	
def Admin_sell_product(request):
	if request.method == 'POST':
		# สมมุติว่าใน form มีข้อมูลสินค้าที่ถูกเลือกมาในรูปแบบ JSON หรือ list
		# ตัวอย่าง: {'items': [{'product_id': 1, 'quantity': 2}, ...], 'payment_type': 'cash'}
		items = request.POST.get('items')  # ควรทำการ parse ข้อมูลให้ถูกต้อง
		payment_type = request.POST.get('payment_type')
		total_price = 0
		
		# สร้างใบสั่งซื้อใหม่
		order = Order.objects.create(
			user=request.user,
			total_price=0,  # จะอัพเดตภายหลัง
			status='pending',
			created_at=timezone.now(),
		)
		
		# ประมวลผลสินค้าในตะกร้า
		for item in items:  # สมมุติว่า items เป็น list ที่ได้มาจากการ parse JSON
			product = Product.objects.get(id=item['product_id'])
			quantity = int(item['quantity'])
			price = product.price
			total_price += price * quantity
			
			OrderItem.objects.create(
				order=order,
				product=product,
				quantity=quantity,
				price=price,
			)
			# อัพเดต stock_qty ของสินค้า
			product.stock_qty -= quantity
			product.save()
		
		# อัพเดตยอดรวมใน order
		order.total_price = total_price
		order.status = 'paid'
		order.save()
		
		# จัดการ Payment ในกรณีที่ต้องการบันทึกการชำระเงิน
		# Payment.objects.create(order=order, payment_type=payment_type, amount=total_price, created_at=timezone.now())
		
		messages.success(request, "การขายสำเร็จแล้ว")
		return redirect('admin_sell_product')  # หรือเปลี่ยนไปยังหน้าที่ต้องการ
	
	# GET request: ดึงรายการสินค้าทั้งหมดสำหรับการเลือกขาย
	products = Product.objects.all()
	context = {
		'products': products,
	}
	return render(request, 'pos/admin_sell_product.html', context)