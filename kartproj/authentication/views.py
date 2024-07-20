from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from .forms import Userforms
from django.http import HttpResponse
# Create your views here.

def register(request):
    if request.method == 'POST':
       form=Userforms(request.POST)
       if form.is_valid():
            form.save()
            # username =form.cleaned_data.get['user']
            messages.success(request,"you have registered")
            return redirect('signin')
           
    else:
        form=Userforms()
    return render(request, 'auth/register.html', {'form':form})

def signin(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        validate = authenticate(request,username=username,password=password)
        if validate is not None:
            login(request,validate)
            messages.success(request,'logged in as' + username + 'successfully')
            return redirect('home')
        else:
            messages.error(request,'you are not a user')
    return render(request,'auth/login.html')

def loggingout(request):
    logout(request)
    messages.success(request,'logged out successfully')
    return redirect('home')

