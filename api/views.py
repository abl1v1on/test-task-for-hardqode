from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from products.utils import get_all_products
from .serializers import ProductSerializer, LessonSerializer
from products.models import Product


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
    Класс представления для получения списка всех уроков связанных
    с конкретным курсом
    """
    def get(self, request, product_url):
        # Получаем объект курса по слагу
        product = get_object_or_404(Product, slug=product_url)
        
        """
        Проверяем, есть ли у пользователей доступ к урокам этого курса. Если нет,
        то возвращаем ошибку. Иначе, возвращаем список уроков
        """
        if not product.is_published:
            return Response(
                {'message': f'Доступ к урокам этого курса станет доступен {product.start_date}'}, 
                status=404)
        serializer = LessonSerializer(product.lessons.all(), many=True)
        return Response(serializer.data)


