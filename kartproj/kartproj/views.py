from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from kartapp.models import *
from django.contrib import messages
from django.http import JsonResponse
import json

# Create your views here.
def category(request):
    collection= Category.objects.filter(status=0)
    context={       
        'collection':collection,
    }
    return render(request,'category.html',context)

def productview(request,name):
    if  Category.objects.filter(name=name).exists():
        product= Product.objects.filter(category__name=name)
    return render(request,'products.html',{'product': product, 'name':name}) 
def productdetails(request,name):
    if Product.objects.filter(name=name).exists():
        detail=Product.objects.get(name=name)
        if Wishlist.objects.filter(product__name = name).exists():
            wish = Wishlist.objects.get(product__name = name)
            check = wish.is_liked
            return render(request,'prductview.html',{'detail':detail, 'check':check } )
        else:
            return render(request, 'prductview.html', {'detail':detail})
def sellerstore(request,name):
    if Product.objects.filter(seller_name=name).exists:
        Store=Product.objects.filter(seller_name=name)
    return render(request,'',{'Store':Store})

def addcart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.load(request)
            qty = int(data['qty'])
            pid = data['pid']
            product_status = Product.objects.get(id=pid)
            if product_status:
                if Cart.objects.filter( user = request.user.id, Product=product_status).exists():
                    return JsonResponse ({'status':'Product is exist in cart'}, status ='200')
                else:
                    if product_status.quantity >= qty:
                        cart= Cart.objects.create(user = request.user,Product=product_status,product_quantity=qty)
                        cart.save()
                        product =  Product.objects.get(id=pid)
                        product.quantity -= qty
                        product.save()
                        messages.success(request, 'Product added successfully')
                        return JsonResponse({'status': 'Product added to cart'},status='200')
                    else:
                        return JsonResponse({'status':'Product out of stock'}, status='200')
        else:
            return JsonResponse({'status': 'login to add cart'},status='200')              
    return JsonResponse({'status':'Invalid Access'},status ='200')
        
@login_required(login_url='auth:login')
def cartview(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        return render(request, 'auth/cart.html', {'cart':cart})
def remove_cart(request,id):
    kart = Cart.objects.get(id=id)
    kart.delete()
    return redirect('cartview')
def wishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data= json.load(request)
            isliked=data['isliked']
            pid = data['pid']
            # return HttpResponse(data['pid'])
            product_status = Product.objects.get(id=pid)
            # return HttpResponse(product_status.id)
            if product_status:
                if Wishlist.objects.filter( user = request.user.id, product=product_status).exists():
                    return JsonResponse({'status':'already exists in wishlist'},status='200')
                else:
                    wish = Wishlist.objects.create(user = request.user,product = product_status,is_liked=isliked)
                    wish.save()
                    messages.success(request, 'we got your wishlist')
                    return JsonResponse({'status':'added to wishlist'},status='200')
            else:
                return JsonResponse ({'status':'product doesnt exists'}, status='200')
        else:
            return JsonResponse({'status':'login to make a wishlist'},status='200')
    else:
        return JsonResponse({'status':'invaild access'},status='200')
                    
                    
@login_required(login_url='auth:login')
def viewWishlist(request):   
    if request.user.is_authenticated:
        user = request.user
        list = Wishlist.objects.filter(user=user)
        return render(request,'auth/wishlist.html',{'list':list})
                    
def remove_wishlist(request,id):
    list= Wishlist.objects.get(id=id)  
    list.delete()
    return redirect('viewwishlist')         


def home(request):
    return render(request,'home.html')


