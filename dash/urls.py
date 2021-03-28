"""iotdash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('product/',views.product,name='product'),
    path('ux/',views.ux,name='ux'),
    path('webservices/',views.webservices,name='webservices'),
    path('iotdevices/',views.iotdevices,name='iotdevices'),
    path('digitaloceanhosting/',views.digitaloceanhosting,name='digitaloceanhosting'),
    path('devops/',views.devops,name='devops'),
    path('dataanalytics/',views.dataanalytics,name='dataanalytics'),
    path('chatmessanger/',views.chatmessanger,name='chatmessanger'),
    path('azurecloudsupport/',views.azurecloudsupport,name='azurecloudsupport'),
    path('awshosting',views.awshosting,name='awshosting'),
    path('awscloudservice',views.awscloudservice,name='awscloudservice'),
    path('appsservices/',views.appsservices,name='appsservices'),
    path('shopsingle/<int:pk>',views.shopSingle,name='shopsingle'),
    path('singleblog/',views.blogSingle,name='singleblog'),
    path('service/',views.services,name='service'),
    path('privacypolicy/',views.privacyPolicy,name='privacypolicy'),
    path('signupLogin/',views.SignUplogin,name='login'),
    path('logout/',views.logout,name='logout'),
    path('search/',views.search,name='search'),
    path('contactUs/',views.contactUs,name='contactUs'),
    path('checkout/',views.checkout,name='checkout'),
    path('thankyou/',views.thankyou,name='thankyou'),
    path('removeitems/',views.removecartItems,name='removeitems'),
    path('addtocart/',views.AddToCart,name='addtocart'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment_done',views.payment_done,name='payment_done'),
    path('payment_cancelled',views.payment_cancelled,name='payment_cancelled'),
]
