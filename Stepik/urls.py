from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from products.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('products/', include('products.urls', namespace='product')),
    path('users/', include('users.urls', namespace='user')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)