from django.urls import path

from .views import RegisterUserView, logout_user, LoginUserView, UserProfile, UpdateProfile

app_name = 'user'


urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('signup/', RegisterUserView.as_view(), name='signup'),
    path('logout/', logout_user, name='logout'),
    path('profile/<int:pk>/', UserProfile.as_view(), name='profile'),
    path('update-profile/<int:pk>/', UpdateProfile.as_view(), name='update_profile'),
]



