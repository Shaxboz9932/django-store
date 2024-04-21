from django.urls import path
from .views import products, basket_add, basket_remove, pagination

app_name = 'products'

urlpatterns = [
    path('', products, name='products'),
    path('category/<int:category_id>/', products, name='category'),
    path('basket/add/<int:product_id>/', basket_add, name='add'),
    path('basket/delete/<int:basket_id>/', basket_remove, name='delete'),
    path('pagination/', pagination, name='pagination')
]
