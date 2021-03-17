from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import  Product,Category,ContactUs
from .models import SignUp
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.core.paginator import Paginator
# Create your views here.
def home(req):
    items=Product.objects.all()
    items=list(items)
    if len(items)>10:
        items=items[:10]
    d={'items':items}
    return render(req,'index.html' , d)
def about(req):
    return render(req,'about.html')
def contact(req):
    return render(req,'contacts.html')
@csrf_exempt
def contactUs(req):
    if req.method=='POST':
        name=req.POST.get('name')
        phone=req.POST.get('phone')
        message=req.POST.get('message')
        email=req.POST.get('email')
        print(name,email,phone,message)
        if email is not None and message is not None and phone is not None and name is not None:

            ContactUs(name=name,email=email,number=phone,message=message).save()
            print("inside contact us")
            return JsonResponse({'success':True})
    print("else part")

    return JsonResponse({'success':False})
def SignUplogin(req):
    if req.method=='POST':
        if 'signup' in req.POST:
            username=req.POST['username']
            email=req.POST['email']
            password=req.POST['password']
            try:
                print(email,username,password)
                if email not in User.objects.filter(email__contains=email):

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
        search_des=Product.objects.filter(description__contains=query)
        search_price=Product.objects.filter(price__contains=query)
        search_cat_des=Category.objects.filter(description__contains=query)
        return render(req,'search.html',{'search_result':search_result,'search_des':search_des,'search_price':search_price,'search_cat_des':search_cat_des})
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
@login_required()
def gallery(req):
    return render(req,'gallery.html'),
def services(req):
    return render(req,'services.html')
def privacyPolicy(req):
    return render(req,'pravicy-policy.html')

