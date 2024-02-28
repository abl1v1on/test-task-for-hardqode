from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from products.utils import get_all_products
from .serializers import ProductSerializer, LessonSerializer
from products.models import Product, Lesson


class ProductListAPIView(APIView):
    """
    Класс представления для получения списка всех объектов из таблицы Product
    """
    def get(self, request):
        products = get_all_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)



class LessonsListAPIView(APIView):
    """
    Класс представления для получения конкретного объекта из таблицы Product
    """
    def get(self, request, product_url):
        product = get_object_or_404(Product, slug=product_url)
        
        """
        В тз сказанно: 
        'API с выведением списка уроков по конкретному продукту 
        к которому пользователь имеет доступ'.
        Как я понимаю, пользователь имеет доступ только к тем курсам, которые уже вышли,
        т.е. is_published True
        """
        if not product.is_published:
            return Response(
                {'message': f'Доступ к урокам этого курса станет доступен {product.start_date}'}, 
                status=404)
        serializer = LessonSerializer(product.lessons.all(), many=True)
        return Response(serializer.data)