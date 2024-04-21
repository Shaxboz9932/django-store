from django.contrib import admin
from .models import ProductCategory, Product, Basket

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)

class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity')

admin.site.register(Basket)

