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

from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('product/',views.product,name='product'),
    path('gallery/',views.gallery,name='gallery'),
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
]
