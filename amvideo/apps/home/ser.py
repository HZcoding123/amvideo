from rest_framework import serializers
from . import models


#  轮播图接口序列化类
class BannerViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Banner
        fields = ['name', 'img', 'link']
