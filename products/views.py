from django.shortcuts import get_object_or_404, redirect, render

from .models import Product
from .utils import get_all_products, add_user_in_group, check_subscription


def index(request):
    """
    Функция представления главной страницы
    """
    # Получаем все курсы
    products = get_all_products()
    
    context = {
        'products': products,
        'title': 'Главная страница'
    }
    return render(request, 'index.html', context)


def product_detail(request, product_url):
    # Получаем объект курса по слагу
    product = get_object_or_404(Product, slug=product_url)
    
    if request.method == 'POST':
        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            return redirect('user:login')
        # Обрабатываем нажатие на кнопку "Записаться на курс"
        if 'buy-product' in request.POST:
            add_user_in_group(product, request.user)
            return redirect('product:lesson', product_url)

    context = {
        'title': product.product_name,
        'product': product, 
        'is_sub': check_subscription(product, request.user)
    }
    return render(request, 'products/product-detail.html', context)


def product_list(request):
    """
    Функция представления страницы списка курсов
    """

    # Получаем все курсы и сортируем в обратном порядке по id
    products = get_all_products().order_by('-id')
    # Получаем параметр сортировки
    sort_by = request.GET.get('sort_by')

    # Проверяем, есть ли параметр сортировки. Если есть, то сортируем по указанному значению
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


def lesson(request, product_url):
    product = get_object_or_404(Product, slug=product_url)
    """
    Проверяем параметр is_published 
    (выключение кнопки на странице курса, не дает гарантии, что никто не захочет 
    перейти к урокам через url). Если он равен False, то перекидываем на страницу 
    информации о курсе, а иначе даем пользователю смотреть уроки
    """

    if not product.is_published:
        return redirect('product:product_detail', product_url=product_url)
    
    current_lesson = request.GET.get('lesson') # Получаем текущий урок
    product_lessons = product.lessons.all() # Получаем все уроки конкретного курса
    lessons_quantity = product_lessons.count() # Кол-во уроков

    # Проверяем, есть ли параметр current_lesson. Если есть, то переключаемся на выбранный урок
    if current_lesson:
        # Если параметр current_lesson больше количества уроков, то перекидываем на страницу информации о курсе
        if int(current_lesson) > lessons_quantity:
            return redirect('product:product_detail', product_url=product_url)
        product_lessons = product_lessons[int(current_lesson) - 1]

    context = {
        'title': product.product_name,
        'lessons': product_lessons,
        'current_lesson': current_lesson,
        'lessons_quantity': lessons_quantity
    }
    return render(request, 'products/lesson.html', context)
