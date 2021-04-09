from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.http import HttpResponse,JsonResponse
from .models import  Product,Category,ContactUs,Cart,OrderTable,Information,Reviews,FAQ,ProductImage
from .models import SignUp
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.core.paginator import Paginator
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from decimal import Decimal
import json
# Create your views here.
def home(req):

    items=Product.objects.filter(cat=1)
    product_list=[]
    for item in items:
        # check if product is already purchase_or not
        if not item.purchase_or_not:
            product_list.append(item)
# only 10 product show in home page
    if len(product_list)>10:
        items=product_list[:10]
    d={'items':items,'cat':Category.objects.all()}
    return render(req,'index.html' , d)
def CategoryShow(req,pk):
    # category wise filter the product
    cat = Category.objects.get(pk=pk)
    product=Product.objects.filter(cat=cat)

    return render(req,'category.html',{'items':product,'cat':Category.objects.all()})
def about(req):
    return render(req,'about.html')
def contact(req):
    return render(req,'contacts.html')
@login_required(login_url='/signupLogin/')
@csrf_exempt
def AddToCart(req):
    print("inside add to cart")
# add to cart
    if req.method=='POST':
        pid=req.POST.get('id')
        if pid is None:
            return JsonResponse({'success':False})
        pid=int(pid)
        print("pid = {}".format(pid))
        is_exist=Cart.objects.filter(product__id=pid,user__id=req.user.id,status=False)
        # check if product is already exist in cart or not
        if len(is_exist)>0:
            return JsonResponse({'success':True})
        else:
            product=get_object_or_404(Product,id=pid)
            user=get_object_or_404(User,id=req.user.id)
            cart=Cart(user=user,product=product)
            cart.save()
            return JsonResponse({'success':True})
    return JsonResponse({'sucess':False})
@login_required(login_url='/signupLogin/')
def checkout(req):
    # list all items in cart and calculate total price
    order_list=[]
    cartItems=Cart.objects.filter(user__id=req.user.id)
    for product in cartItems:
        order_list.append(product.product)
    total=0
    for product in order_list:
        total+=int(product.price)
    if total!=0:
        total+=50
    return render(req,'checkout.html',{'products':order_list,'total':total})
    #return render(req,'SignUp-login.html')
@csrf_exempt
@login_required(login_url='/signupLogin/')
def removecartItems(req):
    # remove item from cart
    print("inside removecartItems")
    if req.method=='POST':

        if req.user.is_authenticated:
            id=req.POST['id']
            print(id)
            cart=get_object_or_404(Cart,product__id=id)
            print(cart)
            if cart is not None:

                cart.delete()
                print('object deleted')
                order_list=[]
                cartItems=Cart.objects.filter(user__id=req.user.id)
                for product in cartItems:
                    order_list.append(product.product)
                total=0
                for product in order_list:
                    total+=int(product.price)
                # add delivery charge
                if total!=0:
                    total+=50
                return JsonResponse({'success':True,'total':total})


    return JsonResponse({'success':False})
@login_required(login_url='/signupLogin/')
def thankyou(req):
    if req.method=='POST':
        email=req.POST['email']
        tel=req.POST['tel']
        full_name=req.POST['name']
        address=req.POST['address']
        city=req.POST['city']
        state=req.POST['state']
        country=req.POST['country']
        poster_code=req.POST['postal']

        items=Cart.objects.filter(user_id__id=req.user.id,status=False)
        amount=0
        products=""
        inv="INV-"
        cart_ids=''
        product_ids=''
        host=req.get_host()
        for j in items:
            products+=str(j.product.name)+"\n"
            amount+=int(j.product.price)
            product_ids+=str(j.product.id)+"\n"
            inv+=str(j.product.id)
            cart_ids+=str(j.id)+','
        if amount!=0:
            amount+=50 # add delivery charge
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': str(amount),
            'item_name': products,
            'invoice': inv,

            'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host,
                                               reverse('payment_done')),
            'cancel_return': 'http://{}{}'.format(host,
                                                  reverse('payment_cancelled')),
        }
        print(email,tel,full_name,address,country,city,state,poster_code)

        user=User.objects.get(username=req.user.username)
        order_table=OrderTable(customer_id=user,cart_ids=cart_ids,products_ids=product_ids,invoice_id=inv , email=email,tel=tel , full_name=full_name,address=address , country=country,city=city,state=state,poster_code=poster_code)
        order_table.save()
        order_table.invoice_id=str(order_table.id)+inv
        order_table.save()
        req.session['order_id']=order_table.id
        form = PayPalPaymentsForm(initial=paypal_dict)

        #return  redirect('https://www.sandbox.paypal.com/webapps/hermes?token=85794313UL176235D&useraction=commit&mfid=1617882715069_b0a4ab53e3ed6')
        return render(req, 'ThankYou.html', { 'form': form})

    return redirect('home')
@login_required(login_url='/signupLogin/')
def payment_done(req):
    if 'order_id' in req.session:
        order_id=req.session['order_id']
        order_obj=get_object_or_404(OrderTable,id=order_id)
        order_obj.status=True
        order_obj.save()
        for i in order_obj.cart_ids.split(',')[:-1]:
            cart_object=Cart.objects.get(id=i)
            cart_object.status=True
            cart_object.save()
            product=Product.objects.filter(id=i)
            product.purchase_or_not=True
            product.save()
    return  HttpResponse("Payment Sucessfull")
@login_required(login_url='/signupLogin/')
def payment_cancelled(req):
    return HttpResponse("Payment Cancel")

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
                message='user alreday exists'
            return render(req,'SignUp-login.html',{'message':message})
        elif 'login' in req.POST:
            print('inside login')
            username=req.POST['Username']
            password=req.POST['Password']
            user = auth.authenticate(username=username,password=password)
            print(user)
            print('inside login')
            if user is not None:
                auth.login(req, user)
                return redirect('home')
            message='invalid email or password'
            return render(req,'SignUp-login.html',{'message':message})



    return render(req,'SignUp-login.html')
def ux(req):
    return render(req,'ux.html')
def webservices(req):
    return render(req,'WebServices.html')
def iotdevices(req):
    return render(req,'IotDevices.html')
def devops(req):
    return render(req,'Devops.html')
def dataanalytics(req):
    return render(req,'DataAnalytics.html')
def digitaloceanhosting(req):
    return render(req,'DigitalOceanHosting.html')
def appsservices(req):
    return render(req,'AppsServices.html')
def awshosting(req):
    return render(req,'AwsHosting.html')
def awscloudservice(req):
    return render(req,'AwsCloudService.html')
def chatmessanger(req):
    return render(req,'ChatMessanger.html')
def azurecloudsupport(req):
    return render(req,'AzureCloudSupport.html')
def search(req):
    if req.method=='GET':
        query=req.GET.get('search')
        if query is None:
            return  render(req,'index.html')
        # search the name in product
        search_result=Product.objects.filter(name__contains=query,purchase_or_not=False)
        # search by description
        search_des=Product.objects.filter(description__contains=query,purchase_or_not=False)
        # search by price
        search_price=Product.objects.filter(price__contains=query,purchase_or_not=False)
        # search in category description
        search_cat_des=Category.objects.filter(description__contains=query)
        return render(req,'search.html',{'search_result':search_result,'search_des':search_des,'search_price':search_price,'search_cat_des':search_cat_des})
    return  render(req,'index.html')
@login_required(login_url='/signupLogin/')
def shopSingle(req,pk):


    product=Product.objects.filter(pk=pk,purchase_or_not=False)
    items=Product.objects.all()

    cartItems=Cart.objects.filter(product__id=pk)
    information=Information.objects.filter(product__id=pk)
    faq=FAQ.objects.filter(product__id=pk)
    reviews=Reviews.objects.filter(product__id=pk)
    images=ProductImage.objects.filter(product__id=pk)
    images=list(images)
    image=Product.objects.filter(id=pk)
    for i in image:
        print(i)
        images.append(i)

    d = {'products': items , 'product': product,'cartItems':cartItems,'information':information,'faq':faq,'review':reviews,'images':images}
    return render(req,'shop-single.html', d)
    #return render(req,'SignUp-login.html')
def product(req):
    items=Product.objects.filter(purchase_or_not=False).order_by('id')
    l=list(items)
    # date wise sort the product
    date_wise_sorted_list=sorted(l,key=lambda x:x.date,reverse=True)
    print(date_wise_sorted_list)
    # Pagination code only 4 item per page
    paginator=Paginator(items,4)
    page_number=req.GET.get('page')
    page_obj=paginator.get_page(page_number)

    d={'items':page_obj,'new_product':date_wise_sorted_list}
    return render(req,'shop.html',d)

@login_required(login_url='/signupLogin/')
def logout(req):
    auth.logout(req)
    return redirect('home')



def privacyPolicy(req):
    return render(req,'pravicy-policy.html')

