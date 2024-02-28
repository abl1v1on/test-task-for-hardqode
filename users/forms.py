from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин', 
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Введите логин'}
            )
        )
    
    password = forms.CharField(
        min_length=8, 
        label='Пароль', 
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Введите пароль'}
            )
        )


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя', 
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Введите логин'}
            )
        )
    
    email = forms.CharField(
        label='Email', 
        widget=forms.EmailInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Введите email'}
            )
        )
    
    password1 = forms.CharField(
        min_length=8, 
        label='Пароль', 
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Введите пароль'}
            )
        )
    
    password2 = forms.CharField(
        min_length=8, 
        label='Повторите пароль', 
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Повторите пароль'}
            )
        )

    sub_to_newsletter = forms.BooleanField(
        label='Подписаться на рассылку',
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input form-control'}
        )
    )

    profile_pic = forms.ImageField(
        label='Аватар',
        widget=forms.FileInput(
            attrs={'class': 'form-control form-control-lg'}
        )
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'sub_to_newsletter', 'profile_pic')

    def clean_email(self):
        """
        Проверяем, существует ли пользователь с таким E-mail
        """
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким E-mail уже существует')
        return email


# class UpdateProfileForm(forms.ModelForm):
#     class Meta:
#         model = get_user_model()
#         fields = ('username', 'email', 'profile_pic')

#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             # 'profile_pic': forms.FileInput(attrs={'class': 'form-control'})
#         }

#         labels = {
#             'profile_pic': ''
#         }