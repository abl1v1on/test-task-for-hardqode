from Stepik.celery import app
from django.core.mail import send_mail
from datetime import datetime
import pytz

from .models import Product, Lesson


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


"""
Таск используется в сигнале и будет отправлять письма о новых уроках
тем пользователям, которые подписаны на курс.
"""
@app.task
def send_mail_about_new_lessons():
    # Крайний урок
    lesson = Lesson.objects.all().last()

    # Пробегаемся циклом по всем группам
    for group in lesson.product.group_product.all():
        # Пробегаемся циклом по всем студентам группы
        for user in group.students.all():
            # Проверяем, подписан ли пользователь на рассылку
            if user.sub_to_newsletter:
                send_mail(
                    'У вас новый урок',
                    f'У вас новый урок: {lesson.lesson_name}.',
                    'djangoTestTask@yandex.ru',
                    [user.email],
                    fail_silently=False
                )

