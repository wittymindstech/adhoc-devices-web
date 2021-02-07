from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(req):
    return render(req,'index.html')
def about(req):
    return render(req,'about.html')
def contact(req):
    return render(req,'contacts.html')
def product(req):
    return render(req,'shop.html')
def gallery(req):
    return render(req,'gallery.html')
