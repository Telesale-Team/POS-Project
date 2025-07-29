from django.shortcuts import render,redirect
from .models import ProfileUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegisterForm

# Create your views here.

def Dashboard(request):
	context = {}
	return render(request, 'staff/dashboard.html',context)

def Account_Profile(request):
    context = {         
        }
    return render(request, 'account/account.html', context)

def Forgot_Password (request):
    return render(request,'account/forgot-password.html')

def User_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('blogs')
    return render(request, 'account/login.html')

def User_logout(request):
    logout(request)
    return redirect('login')

def Register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'account/register.html')


