from django.shortcuts import get_object_or_404, render

from .models import Product


def index(request):
    products = Product.objects.all()
    
    context = {
        'products': products,
        'title': 'Главная страница'
    }
    return render(request, 'index.html', context)


def product_detail(request, product_url):
    product = get_object_or_404(Product, slug=product_url)

    context = {
        'title': product.product_name,
        'product': product
    }
    return render(request, 'products/product-detail.html', context)


def product_list(request):
    products = Product.objects.all().order_by('-id')
    # Получаем параметр сортировки
    sort_by = request.GET.get('sort_by')

    # Проверяем, есть ли параметр сортировки, и если есть, то сортируем
    if sort_by:
        if sort_by == 'price':
            products = products.order_by('price')
        elif sort_by == '-price':
            products = products.order_by('-price')
        elif sort_by == 'start_date':
            products = products.order_by('start_date')

    context = {
        'products': products,
        'title': 'Список курсов',
        'sort_by': sort_by
    }
    return render(request, 'products/product-list.html', context)
