from Stepik.celery import app
from datetime import datetime
import pytz
from .models import Product


"""
Такса будет работать в фоновом режиме и проверяет, 
совпадает ли сегодняшняя дата с той, которая указана
в поле start_date модели Product. Если даты совпадают, то 
is_published становиться True и все авторизованные пользователи 
получат доступ к курсу. Timezone поставил ЕКБ, так как мне удобнее 
тестировать с местным временем. Примитивное решение с datetime
""" 
@app.task
def update_is_published():
    # Текущая дата
    current_date = datetime.now().astimezone(pytz.timezone('Asia/Yekaterinburg')).date()
    """
    Пробегаемся циклом по всем объектам модели Product,
    конвертируем значение поля start_date в объект datetime
    и сравниваем с текущей датой. Если текущая дата больше или равна
    start_date, то мы меняем поле is_published на True
    """
    for product in Product.objects.all():
        product_start_date = datetime.strptime(str(product.start_date), '%Y-%m-%d').date()

        if current_date >= product_start_date:
            product.is_published = True
            product.save()
