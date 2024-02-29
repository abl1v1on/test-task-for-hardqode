from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import RegisterUserForm, LoginUserForm, UpdateProfileForm


class LoginUserView(LoginView):
    """
    Страница авторизации пользователя
    """
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterUserView(CreateView):
    """
    Страница регистрации пользователя
    """
    form_class = RegisterUserForm
    template_name = 'users/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация' 
        return context
    
    def get_success_url(self):
        return reverse_lazy('user:login')


class UserProfile(DetailView):
    """
    Страница профиля пользователя
    """
    model = get_user_model()
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Профиль пользователя {self.object.username}'
        return context



class UpdateProfile(UpdateView):
    """
    Изменение информации о пользователе
    """
    model = get_user_model()
    template_name = 'users/update-profile.html'
    form_class = UpdateProfileForm

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля {self.object.username}'
        return context

    def get_success_url(self):
        return reverse_lazy('user:profile', kwargs={'pk': self.object.pk})
    
    def get(self, request, *args, **kwargs):
        """
        Делаем проверку, чтобы пользователи 
        не могли обратиться к чужому профилю через url 
        """
        if request.user.pk == kwargs['pk']:
            return super().get(request, *args, **kwargs)
        return redirect('home')


def logout_user(request):
    logout(request)
    return redirect('home')
