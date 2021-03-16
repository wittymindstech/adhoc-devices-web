from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models import CASCADE
# Create your models here.
class Category(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()

    def __str__(self):
        return self.title
class Product(models.Model):
    date=models.DateTimeField(auto_now_add=True,null=True)
    name=models.CharField(max_length=200)
    description=models.TextField()
    price=models.CharField(max_length=50)
    cat=models.ForeignKey(Category,on_delete=models.CASCADE)
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
class SignUp(models.Model):
    user=models.ForeignKey(to=User,on_delete=CASCADE,null=True)


    def __str__(self):
        return self.user
