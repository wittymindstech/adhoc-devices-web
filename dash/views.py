from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, JsonResponse
from .models import (Product, Category,
                     ContactUs, Cart,
                     OrderTable, Information,
                     Reviews, FAQ, ProductImage)
from .models import SignUp
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from decimal import Decimal
import json
from django.views.generic import TemplateView
from django.core.mail import send_mail

# Create your views here.


def home(request):
    d = {'cat': Category.objects.all()[0:6]}
    return render(request, 'index.html', d)


def CategoryShow(request, slug):
    # category wise filter the product
    cat = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(cat=cat.id)
    all_products = Product.objects.all()
    categories = Category.objects.all()
    context = {'products': products,
               'cat': cat,
               'all_products': all_products,
               'categories': categories}
    return render(request, 'category.html', context)


@login_required(login_url='/signupLogin/')
@csrf_exempt
def AddToCart(request):
    print("inside add to cart")
    # add to cart
    if request.method == 'POST':
        pid = request.POST.get('id')
        if pid is None:
            return JsonResponse({'success': False})
        pid = int(pid)
        print("pid = {}".format(pid))
        is_exist = Cart.objects.filter(product__id=pid, user__id=request.user.id, status=False)
        # check if product is already exist in cart or not
        if len(is_exist) > 0:
            return JsonResponse({'success': True})
        else:
            product = get_object_or_404(Product, id=pid)
            user = get_object_or_404(User, id=request.user.id)
            cart = Cart(user=user, product=product)
            cart.save()
            total = 0
            for item in cart:
                if item.price:
                    total += item.price
            request.session['total'] = total
            return JsonResponse({'success': True})
    return JsonResponse({'sucess': False})


@login_required(login_url='/signupLogin/')
def checkout(request):
    # list all items in cart and calculate total price
    order_list = []
    cartItems = Cart.objects.filter(user__id=request.user.id)
    for product in cartItems:
        order_list.append(product.product)
    total = 0
    for product in order_list:
        total += int(product.price)
    if total != 0:
        total += 50
    request.session['total'] = total
    return render(request, 'checkout.html', {'products': order_list, 'total': total})


@csrf_exempt
@login_required(login_url='/signupLogin/')
def removecartItems(request):
    # remove item from cart
    print("inside removecartItems")
    if request.method == 'POST':
        if request.user.is_authenticated:
            id = request.POST['id']
            print(id)
            cart = get_object_or_404(Cart, product__id=id)
            print(cart)
            if cart is not None:

                cart.delete()
                print('object deleted')
                order_list = []
                cartItems = Cart.objects.filter(user__id=request.user.id)
                for product in cartItems:
                    order_list.append(product.product)
                total = 0
                for product in order_list:
                    total += int(product.price)
                # add delivery charge
                if total != 0:
                    total += 50
                request.session['total'] = total
                return JsonResponse({'success': True, 'total': total})

    return JsonResponse({'success': False})


@login_required(login_url='/signupLogin/')
def order_complete(request):
    if request.method == 'POST':
        email = request.POST['email']
        tel = request.POST['tel']
        full_name = request.POST['name']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        poster_code = request.POST['postal']

        items = Cart.objects.filter(user_id__id=request.user.id, status=False)
        amount = 0
        products = ""
        inv = "INV-"
        cart_ids = ''
        product_ids = ''
        host = request.get_host()
        for j in items:
            products += str(j.product.name) + "\n"
            amount += int(j.product.price)
            product_ids += str(j.product.id) + "\n"
            inv += str(j.product.id)
            cart_ids += str(j.id) + ','
        if amount != 0:
            amount += 50  # add delivery charge
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': str(amount),
            'item_name': products,
            'invoice': inv,

            'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host,
                                               reverse('payment_done')),
            'cancel_return': 'http://{}{}'.format(host,
                                                  reverse('payment_cancelled')),
        }
        print(email, tel, full_name, address, country, city, state, poster_code)

        user = User.objects.get(username=request.user.username)
        order_table = OrderTable(customer_id=user, cart_ids=cart_ids, products_ids=product_ids, invoice_id=inv,
                                 email=email, tel=tel, full_name=full_name, address=address, country=country, city=city,
                                 state=state, poster_code=poster_code)
        order_table.save()
        order_table.invoice_id = str(order_table.id) + inv
        order_table.save()
        request.session['order_id'] = order_table.id
        form = PayPalPaymentsForm(initial=paypal_dict)

        # return  redirect('https://www.sandbox.paypal.com/webapps/hermes?token=85794313UL176235D&useraction=commit&mfid=1617882715069_b0a4ab53e3ed6')
        return render(request, 'ThankYou.html', {'form': form})

    return redirect('home')


@login_required(login_url='/signupLogin/')
def payment_done(request):
    if 'order_id' in request.session:
        order_id = request.session['order_id']
        order_obj = get_object_or_404(OrderTable, id=order_id)
        order_obj.status = True
        order_obj.save()
        for i in order_obj.cart_ids.split(',')[:-1]:
            cart_object = Cart.objects.get(id=i)
            cart_object.status = True
            cart_object.save()
            product = Product.objects.filter(id=i)
            product.purchase_or_not = True
            product.save()
    return HttpResponse("Payment Sucessfull")


def contactUs(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')[-10:]
        message = request.POST.get('message')
        email = request.POST.get('email')
        subject = "Adhoc Devices Customer Request"
        print(name, email, phone, message)
        email_template = f"Hello,\n{message}\n From"
        if name != '' and phone != '' \
                and message != '' and email != '' \
                and message != '':
            ContactUs(name=name, email=email, number=phone, message=message).save()
            # todo  "Add Email Sending"
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, [email])
            return JsonResponse({'success': True})
    print("else part")

    return JsonResponse({'success': False})


def SignUplogin(request):
    if request.method == 'POST':
        if 'signup' in request.POST:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            try:
                print(email, username, password)
                if email not in User.objects.filter(email__contains=email):
                    user = User.objects.create_user(email=email, password=password, username=email)
                    print('user created')
                    SignUp.objects.create(user=user)
                    auth.login(request, user)
                    return redirect('home')
            except:
                print("something went wrong")
                message = 'user alreday exists'
            return render(request, 'SignUp-login.html', {'message': message})
        elif 'login' in request.POST:
            print('inside login')
            username = request.POST['Username']
            password = request.POST['Password']
            user = auth.authenticate(username=username, password=password)
            print(user)
            print('inside login')
            if user is not None:
                auth.login(request, user)
                return redirect('home')
            message = 'invalid email or password'
            return render(request, 'SignUp-login.html', {'message': message})

    return render(request, 'SignUp-login.html')


def search(request):
    if request.method == 'GET':
        query = request.GET.get('search')
        if query is None:
            return render(request, 'index.html')
        # search the name in product
        search_result = Product.objects.filter(name__contains=query, purchase_or_not=False)
        # search by description
        search_des = Product.objects.filter(description__contains=query, purchase_or_not=False)
        # search by price
        search_price = Product.objects.filter(price__contains=query, purchase_or_not=False)
        # search in category description
        search_cat_des = Category.objects.filter(description__contains=query)
        return render(request, 'search.html',
                      {'search_result': search_result, 'search_des': search_des, 'search_price': search_price,
                       'search_cat_des': search_cat_des})
    return render(request, 'index.html')


@login_required(login_url='/signupLogin/')
def shopSingle(request, slug):
    product = Product.objects.filter(slug=slug, purchase_or_not=False)
    items = Product.objects.all()

    cartItems = Cart.objects.filter(product__slug=slug)
    information = Information.objects.filter(product__slug=slug)
    faq = FAQ.objects.filter(product__slug=slug)
    reviews = Reviews.objects.filter(product__slug=slug)
    images = ProductImage.objects.filter(product__slug=slug)
    images = list(images)
    image = Product.objects.filter(slug=slug)
    for i in image:
        print(i)
        images.append(i)

    context = {'products': items, 'product': product, 'cartItems': cartItems, 'information': information, 'faq': faq,
               'review': reviews, 'images': images}
    return render(request, 'shop-single.html', context)


def product(request):
    items = Product.objects.filter(purchase_or_not=False).order_by('id')
    l = list(items)
    # date wise sort the product
    date_wise_sorted_list = sorted(l, key=lambda x: x.date, reverse=True)
    print(date_wise_sorted_list)
    # Pagination code only 4 item per page
    paginator = Paginator(items, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'items': page_obj,
               'categories': Category.objects.all(),
               'new_product': date_wise_sorted_list}
    return render(request, 'shop.html', context)


@login_required(login_url='/signupLogin/')
def logout(request):
    auth.logout(request)
    return redirect('home')


@login_required(login_url='/signupLogin/')
def payment_cancelled(request):
    return HttpResponse("Payment Cancel")


class PrivacyPolicyView(TemplateView):
    template_name = 'pravicy-policy.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contacts.html'


class UxCategoryView(TemplateView):
    template_name = 'ux.html'


class WebservicesView(TemplateView):
    template_name = 'WebServices.html'


class IotdevicesView(TemplateView):
    template_name = 'IotDevices.html'


class DevopsView(TemplateView):
    template_name = 'Devops.html'


class DataanalyticsView(TemplateView):
    template_name = 'DataAnalytics.html'


class DigitaloceanhostingView(TemplateView):
    template_name = 'DigitalOceanHosting.html'


class AppsservicesView(TemplateView):
    template_name = 'AppsServices.html'


class AwshostingView(TemplateView):
    template_name = 'AwsHosting.html'


class AwscloudserviceView(TemplateView):
    template_name = 'AwsCloudService.html'


class ChatmessangerView(TemplateView):
    template_name = 'ChatMessanger.html'


class AzurecloudsupportView(TemplateView):
    template_name = 'AzureCloudSupport.html'
