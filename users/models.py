from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    """
    Расширяем базовую модель User
    """
    profile_pic = models.ImageField(upload_to='profile_pics/%Y/%m', 
                                    verbose_name='Аватар', null=True, blank=True)
    profile_desc = models.CharField(max_length=700, 
                                    verbose_name='О себе', null=True, blank=True)
    sub_to_newsletter = models.BooleanField(default=True, 
                                            verbose_name='Подписаться на рассылку')
