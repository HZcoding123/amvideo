from django.db import models
from amvideo.utils.basemodel import BaseModel


# Create your models here.
class Banner(BaseModel):
    img = models.ImageField(upload_to='banner', verbose_name='轮播图', null=True)
    name = models.CharField(max_length=32, verbose_name='轮播图名称')
    link = models.CharField(max_length=32, verbose_name='跳转链接')
    info = models.CharField(max_length=64, verbose_name='图片简介')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name