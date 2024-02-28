from django.urls import path

from .views import RegisterUserView, logout_user, LoginUserView

app_name = 'user'


urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('signup/', RegisterUserView.as_view(), name='signup'),
    path('logout/', logout_user, name='logout'),
]



