from rest_framework import serializers

from products.models import Product, Lesson


class ProductSerializer(serializers.ModelSerializer):
    lessons_quantity = serializers.SerializerMethodField()

    def get_lessons_quantity(slef, obj):
        return obj.lessons.count()
    
    class Meta:
        model = Product
        fields = '__all__'



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
