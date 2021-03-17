from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import  Product
from .models import SignUp
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.core.paginator import Paginator
# Create your views here.
def home(req):
    items=Product.objects.all()
    d={'items':items}
    return render(req,'index.html' , d)
def about(req):
    return render(req,'about.html')
def contact(req):
    return render(req,'contacts.html')
def SignUplogin(req):
    if req.method=='POST':
        if 'signup' in req.POST:
            username=req.POST['username']
            email=req.POST['email']
            password=req.POST['password']
            try:
                print(email,username,password)
                user=User.objects.create_user(email=email,password=password,username=email)
                print('user created')
                SignUp.objects.create(user=user)
                auth.login(req,user)
                return redirect('home')
            except :

                print("something went wrong")
            return render(req,'index.html')
        elif 'login' in req.POST:
            username=req.POST['Username']
            password=req.POST['Password']
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(req, user)
        return redirect('home')



    return render(req,'SignUp-login.html')
def search(req):
    if req.method=='GET':
        query=req.GET.get('search')
        search_result=Product.objects.filter(name__contains=query)
        return render(req,'search.html',{'search_result':search_result})
    return  render(req,'index.html')
def shopSingle(req,pk):
    product=Product.objects.filter(pk=pk)
    items=Product.objects.all()
    for p in product:
        print(p.price)
    d = {'products': items , 'product': product}
    return render(req,'shop-single.html', d)
def product(req):
    items=Product.objects.all().order_by('id')
    l=list(items)
    date_wise_sorted_list=sorted(l,key=lambda x:x.date,reverse=True)
    print(date_wise_sorted_list)
    paginator=Paginator(items,4)
    page_number=req.GET.get('page')
    page_obj=paginator.get_page(page_number)

    d={'items':page_obj,'new_product':date_wise_sorted_list}
    return render(req,'shop.html',d)
@login_required()
def logout(req):
    auth.logout(req)
    return redirect('home')
def blogSingle(req):
    return  render(req,'sindle-blog.html')
def gallery(req):
    return render(req,'gallery.html'),
def services(req):
    return render(req,'services.html')
def privacyPolicy(req):
    return render(req,'pravicy-policy.html')

