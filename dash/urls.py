from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:slug>/', views.CategoryShow, name='category'),
    path('products/', views.product, name='product'),
    path('shopsingle/<slug:slug>', views.shopSingle, name='shopsingle'),
    # path('singleblog/',views.blogSingle,name='singleblog'),
    # path('service/',views.services,name='service'),
    path('signupLogin/', views.SignUplogin, name='login'),
    path('logout/', views.logout, name='logout'),
    path('search/', views.search, name='search'),
    path('contactUs/', views.contactUs, name='contactUs'),
    path('checkout/', views.checkout, name='checkout'),
    path('thankyou/', views.order_complete, name='thankyou'),
    path('removeitems/', views.removecartItems, name='removeitems'),
    path('addtocart/', views.AddToCart, name='addtocart'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment_done', views.payment_done, name='payment_done'),
    path('payment_cancelled', views.payment_cancelled, name='payment_cancelled'),

    # Generic Class Based Views
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('privacypolicy/', views.PrivacyPolicyView.as_view(), name='privacypolicy'),
    path('ux/', views.UxCategoryView.as_view(), name='ux'),
    path('webservices/', views.WebservicesView.as_view(), name='webservices'),
    path('iotdevices/', views.IotdevicesView.as_view(), name='iotdevices'),
    path('digitaloceanhosting/', views.DigitaloceanhostingView.as_view(), name='digitaloceanhosting'),
    path('devops/', views.DevopsView.as_view(), name='devops'),
    path('dataanalytics/', views.DataanalyticsView.as_view(), name='dataanalytics'),
    path('chatmessanger/', views.ChatmessangerView.as_view(), name='chatmessanger'),
    path('azurecloudsupport/', views.AzurecloudsupportView.as_view(), name='azurecloudsupport'),
    path('awshosting', views.AwshostingView.as_view(), name='awshosting'),
    path('awscloudservice', views.AwscloudserviceView.as_view(), name='awscloudservice'),
    path('appsservices/', views.AppsservicesView.as_view(), name='appsservices'),

]
