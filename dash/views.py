from django.shortcuts import render
from django.http import HttpResponse
from .models import  Product
# Create your views here.
def home(req):
    items=Product.objects.all()
    d={'items':items}
    return render(req,'index.html',d)
def about(req):
    return render(req,'about.html')
def contact(req):
    return render(req,'contacts.html')

def product(req):
    items=Product.objects.all()
    l=list(items)
    date_wise_sorted_list=sorted(l,key=lambda x:x.date,reverse=True)
    print(date_wise_sorted_list)
    d={'items':items,'new_product':date_wise_sorted_list}
    return render(req,'shop.html',d)
def gallery(req):
    return render(req,'gallery.html')
