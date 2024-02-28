from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('product-list/', views.ProductListAPIView.as_view(), name='product-list'),
    path('lessons-list/<slug:product_url>/', views.LessonsListAPIView.as_view(), name='lessons-list'),
]
