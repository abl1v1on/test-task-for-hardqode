from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


# Модель курсов
class Product(models.Model):
    product_name = models.CharField('Название', max_length=120)
    description = models.TextField('Описание')
    start_date = models.DateField('Дата начала')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    author = models.ForeignKey(get_user_model(), verbose_name='Автор', 
                               on_delete=models.CASCADE)
    product_cover = models.ImageField('Обложка', upload_to='product_covers/%Y')
    slug = models.SlugField('URL', max_length=120, unique=True, db_index=True)
    max_student_quantity = models.PositiveIntegerField(
        'Максимальное количество студентов в группе',
        default=5
    )
    is_published = models.BooleanField('Опубликован', default=False)

    class Meta:
        db_table = 'product'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.product_name
    
    def get_absolute_url(self):
        return reverse('product:product_detail', kwargs={'product_url': self.slug})
    
    

# Модель уроков
class Lesson(models.Model):
    lesson_name = models.CharField('Название', max_length=120)
    video_content = models.FileField('Видео', upload_to='videos/%Y')
    product = models.ForeignKey(Product, verbose_name='Товар', 
                                on_delete=models.CASCADE, related_name='lessons')

    class Meta:
        db_table = 'lesson'
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.lesson_name


# Модель групп
class Group(models.Model):
    group_name = models.CharField('Название группы', max_length=120)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                                verbose_name='Продукт', related_name='group_product')
    students = models.ManyToManyField(get_user_model(), 
                                      verbose_name='Студенты', related_name='group_student')
    
    class Meta:
        db_table = 'group'
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.group_name
