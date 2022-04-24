from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    telephone = models.CharField(max_length=11, verbose_name='手机号')
    icon = models.ImageField(upload_to='icon', default='default.png', verbose_name='用户头像')

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

