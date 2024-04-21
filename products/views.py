from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import TemplateView, ListView
from .models import Product, ProductCategory, Basket

class IndexView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['title'] = 'Store'

# def index(request):
#     return render(request, 'products/index.html')

# class ProductListView(ListView):
#     model = Product
#     template_name = 'products/products.html'
#     paginate_by = 3
#
#     def get_queryset(self):
#         queryset = super(ProductListView, self).get_queryset()
#         category_id = self.kwargs.get('category_id')
#         return queryset.filter(category_id=category_id) if category_id else queryset
#
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(ProductListView, self).get_context_data()
#         context['title'] = 'Store - Katalog'
#         context['categories'] = ProductCategory.objects.all()
#         return context

def products(request, category_id=None):
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    paginator = Paginator(products, 3)
    page_num = request.GET.get('p', 1)
    page_objects = paginator.get_page(page_num)

    context = {
        'title': 'Store - Katalog',
        'products': page_objects,
        'categories': ProductCategory.objects.all(),
        'page_obj': page_objects,
        'pag': paginator
    }
    return render(request, 'products/products.html', context)

@login_required
def basket_add(request, product_id):
    product = Product.objects.get(pk=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(reverse('products:products'))

@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(pk=basket_id)
    basket.delete()
    return HttpResponseRedirect(reverse('users:profile'))


def pagination(request):
    obj = ['John', 'Paul', 'George', 'Kelvin', 'Max', 'Luisa', 'Anna', 'Danny', 'Mark']
    paginator = Paginator(obj, 2)
    page_num = request.GET.get('p', 1)
    page_objects = paginator.get_page(page_num)

    return render(request, 'products/paginator.html', {'page_obj': page_objects, 'pag': paginator})
