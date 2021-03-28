from django.db import models

from django.contrib.auth.models import User
from django.db.models import CASCADE
# Create your models here.
class Category(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    Image=models.ImageField(upload_to='images',blank=True,null=True)
    def __str__(self):
        return self.title
class Product(models.Model):
    date=models.DateTimeField(auto_now_add=True,null=True)
    name=models.CharField(max_length=200)
    description=models.TextField()
    price=models.CharField(max_length=50)
    cat=models.ForeignKey(Category,on_delete=models.CASCADE)
    purchase_or_not=models.BooleanField(default=False)
    Image=models.ImageField(upload_to='images',blank=True,null=True)
    def __str__(self):
        return  self.name
class ContactUs(models.Model):
    name=models.CharField(max_length=100)
    number=models.CharField(max_length=10)
    email=models.EmailField();
    message=models.TextField();
    def __str__(self):
        return self.name
class OrderTable(models.Model):
    customer_id=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    cart_ids=models.CharField(max_length=100,null=True)
    products_ids=models.CharField(max_length=250,null=True)
    invoice_id=models.CharField(max_length=250,null=True)
    status=models.BooleanField(default=False)
    processed_on=models.DateTimeField(auto_now_add=True,null=True)
    email=models.EmailField(null=True)
    tel=models.CharField(max_length=20,null=True)
    full_name=models.CharField(max_length=100,null=True)
    address=models.TextField(null=True)
    city=models.CharField(max_length=100,null=True)
    state=models.CharField(max_length=100,null=True)
    country=models.CharField(max_length=250,null=True)
    poster_code=models.CharField(max_length=10,null=True)
    def __str__(self):
        return self.cart_ids
class SignUp(models.Model):
    user=models.ForeignKey(to=User,on_delete=CASCADE,null=True)


    def __str__(self):
        return self.user
class Information(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    information=models.TextField(null=True)
    def __str__(self):
        return self.product.name

class FAQ(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    question=models.CharField(max_length=500,null=True)
    answer=models.CharField(max_length=500,null=True)
    def __str__(self):
        return self.product.name
class Reviews(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    reviews=models.TextField(null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    def __str__(self):
        return self.product.name
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    added_on=models.DateTimeField(auto_now_add=True,null=True)
    update_on=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user