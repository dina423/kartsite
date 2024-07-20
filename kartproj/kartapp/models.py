from django.db import models
import os
import datetime
from django.contrib.auth.models import User

def getFileName(request,filename):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_filename='%s%s'%(now_time,filename)
    return os.path.join('uploads',new_filename)    

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=125,null=False)
    images=models.ImageField(upload_to=getFileName, null=True )
    description = models.TextField(max_length=200,)
    status=models.BooleanField(default=False,help_text="0-show,1-hidden")
    created_at=models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return self.name

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=250,null=False)
    seller_name=models.CharField(max_length=125,null=False)
    seller_id=models.CharField(max_length=8,null=False)
    product_images=models.ImageField(upload_to=getFileName, null=True )
    quantity=models.IntegerField(null=False,blank=False)
    original_price=models.FloatField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False)
    description = models.TextField(max_length=200,)
    status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    trending=models.BooleanField(default=False,help_text="0-show,1-Trending")
    created_at=models.DateTimeField(auto_now_add=True)
    rating = models.CharField(max_length=20, blank=True, null=False)
    offer = models.CharField(max_length=20, blank=True, null=False)
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_quantity = models.IntegerField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    @property
    def total_price(self):
        return self.product_quantity * self.Product.selling_price
    
class Wishlist(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE)  
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_liked= models.BooleanField(default=False,help_text="0-unfill,1-fill")
    
    