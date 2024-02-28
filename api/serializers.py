from rest_framework import serializers

from products.models import Product, Lesson


class ProductSerializer(serializers.ModelSerializer):
    lessons_quantity = serializers.SerializerMethodField()
    students_quantity = serializers.SerializerMethodField()
    group_occupancy_percentage = serializers.SerializerMethodField()

    # % заполнения всех групп
    def get_group_occupancy_percentage(self, obj):
        group_fullness = []

        for i in obj.group_product.all():
            group_fullness.append(i.students.count() / obj.max_student_quantity * 100)
    
        return sum(group_fullness) / len(group_fullness) if len(group_fullness) > 0 else 0
    
    # Получаем кол-во учеников занимающихся на продукте 
    def get_students_quantity(self, obj):
        res = 0

        for group in obj.group_product.all():
            res += group.students.count()
        return res
    
    # Получаем количество уроков на продукте
    def get_lessons_quantity(slef, obj):
        return obj.lessons.count()
    
    class Meta:
        model = Product
        fields = '__all__'



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
