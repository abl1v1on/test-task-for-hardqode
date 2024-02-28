from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product, Group, Lesson

class ProductLessonInline(admin.TabularInline):
    """
    Инлайн позволит нам удобно добавлять/удалять уроки
    в админке прямо на странице редактирования курса
    """
    model = Lesson


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'get_cover', 'start_date', 'price', 'author')
    list_display_links = ('product_name', 'get_cover')
    search_fields = ('product_name', )
    prepopulated_fields = {'slug': ('product_name', )} # Автоматическое заполнение поля slug 
    inlines = [ProductLessonInline]

    @admin.display(description='Обложка')
    def get_cover(self, obj: Product):
        """
        Отображаем обложку курса в админке
        """
        return mark_safe(f'<img src="{obj.product_cover.url}" width="200px">')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'product')
    list_display_links = ('group_name', )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('lesson_name', 'product')
    list_display_links = ('lesson_name', )
    
    