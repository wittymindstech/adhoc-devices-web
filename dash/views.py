from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, JsonResponse
from .models import (Product, Category,
                     ContactUs, Cart, SignUp,
                     OrderTable, Information,
                     Reviews, FAQ, ProductImage)
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # For Function Based Views
from django.contrib.auth.mixins import LoginRequiredMixin  # For Class BAsed Views
from django.contrib.auth.models import User, auth
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView, ListView
import uuid
import re

# Create your views here.


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
            products = get_object_or_404(Product, id=pid)
            user = get_object_or_404(User, id=request.user.id)
            cart = Cart(user=user, product=products)
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
    for products in cartItems:
        order_list.append(products.product)
    total = 0
    for products in order_list:
        total += int(products.price)
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
            product_id = request.POST['id']
            print(product_id)
            cart = get_object_or_404(Cart, product__id=product_id)
            print(cart)
            if cart is not None:

                cart.delete()
                print('object deleted')
                order_list = []
                cartItems = Cart.objects.filter(user__id=request.user.id)
                for products in cartItems:
                    order_list.append(products.product)
                total = 0
                for products in order_list:
                    total += int(products.price)
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
        for j in items:
            products += str(j.product.name) + "\n"
            amount += int(j.product.price)
            product_ids += str(j.product.id) + "\n"
            inv += str(j.product.id)
            cart_ids += str(j.id) + ','
        if amount != 0:
            amount += 50  # add delivery charge
            # todo Create Razorpay charge here
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
            products = Product.objects.filter(id=i)
            products.purchase_or_not = True
            products.save()
    return HttpResponse("Payment Sucessfull")


def contactUs(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')[-10:]
        message = request.POST.get('message')
        email = request.POST.get('email')
        subject = "Adhoc Devices Customer Request"
        cleaned_message = re.sub("[^a-zA-Z0-9\n\.\"\&]", '', message)  # Just to be extra cautious
        email_template = f"Hello,\n{cleaned_message}\n\nFrom: {name}\nEmail: {email}\nContact: {phone}"
        if name != '' and phone != '' \
                and message != '' and email != '' \
                and message != '':
            ContactUs(name=name, email=email, number=phone, message=message).save()
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, email_template, email_from, [email])
            return JsonResponse({'success': True})
    print("else part")

    return JsonResponse({'success': False})


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
                      {'search_result': search_result, 'search_des': search_des,
                       'search_price': search_price,
                       'search_cat_des': search_cat_des})
    return render(request, 'index.html')


@login_required(login_url='/signupLogin/')
def shopSingle(request, slug):
    current_product = Product.objects.filter(slug=slug, purchase_or_not=False)
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

    context = {'products': items, 'product': current_product,
               'cartItems': cartItems, 'information': information,
               'faq': faq, 'review': reviews, 'images': images}
    return render(request, 'shop-single.html', context)


def product(request):
    items = Product.objects.filter(purchase_or_not=False).order_by('id')
    # date wise sort the product
    date_wise_sorted_list = sorted(list(items), key=lambda x: x.date, reverse=True)
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


def SignUplogin(request):
    if request.method == 'POST':
        if 'signup' in request.POST:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            try:
                print(email, username, password)
                if User.objects.filter(username=username).first():
                    messages.warning(request, 'Username is taken.')
                    print("test one")
                    return redirect('login')

                if User.objects.filter(email=email).first():
                    messages.warning(request, 'Email is taken.')
                    print("test two")
                    return redirect('login')

                user_obj = User(username=username, email=email)
                user_obj.set_password(password)
                print("I am here!")
                user_obj.save()
                auth_token = str(uuid.uuid4())
                profile_obj = SignUp.objects.create(user=user_obj, auth_token=auth_token)
                send_mail_after_registration(request, email, auth_token)
                # To avoid any issue occur Before creating new user
                print("mail sent")
                profile_obj.save()
                return redirect('home')
            except Exception as e:
                print(f"\nsomething went wrong\n{e}\n\n")
                messages.error(request, 'Something Went Wrong, Please Try again!')
            print("its a get request")
            return render(request, 'SignUp-login.html')
        elif 'login' in request.POST:
            print('inside login')
            username = request.POST['Username']
            password = request.POST['Password']
            user_obj = User.objects.filter(username=username).first()
            if user_obj is None:
                messages.success(request, 'User not found.')
                return redirect('login')

            profile_obj = SignUp.objects.filter(user=user_obj).first()

            # noinspection PyBroadException
            try:
                if not profile_obj.is_verified:
                    # messages.success(request, 'Profile is not verified check your mail.')
                    return redirect('login')
            except:
                user = auth.authenticate(username=username, password=password)
                if user is None:
                    # messages.success(request, 'Wrong password.')
                    return redirect('login')
                auth.login(request, user)
                return redirect('home')
    return render(request, 'SignUp-login.html')


# noinspection PyArgumentList
def verify(request, auth_token):
    try:
        profile_obj = SignUp.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                auth.login(request, user=profile_obj.user)
                return redirect('home')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            auth.login(request, user=profile_obj.user)
            return redirect('home', messages)
        else:
            messages.add_message(request, 'Something went wrong')
            return redirect('home')
    except Exception as e:
        print(e)
        return redirect('home')


def send_mail_after_registration(request, email, token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account: https://{get_current_site(request)}/verify-email/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


class HomeView(ListView):
    template_name = 'index.html'
    queryset = Category.objects.all()[0:6]
    context_object_name = 'cat'


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
