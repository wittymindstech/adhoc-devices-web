from django.contrib import admin
from .models import (Product, Category, SignUp,
                     ContactUs, Cart, OrderTable,
                     Information, Reviews, FAQ,
                     ProductImage)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'price', 'cat', 'purchase_or_not']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(SignUp)
admin.site.register(ContactUs)
admin.site.register(Cart)
admin.site.register(OrderTable)
admin.site.register(Information)
admin.site.register(Reviews)
admin.site.register(FAQ)
admin.site.register(ProductImage)
# Register your models here.
