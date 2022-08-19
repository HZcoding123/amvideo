from rest_framework.generics import GenericAPIView
from . import models
from django.conf import settings
from . import ser
from amvideo.utils.myresponse import Myresponse
from celery_task.banner import banner_update
from django.core.cache import cache
# Create your views here.


# 轮播图视图类
class BannerView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        banner_list = cache.get('banner_list')
        # print('banner_list:', banner_list)
        if not banner_list:
            banner_update.delay()
            banner_list = cache.get('banner_list')
        return Myresponse(data=banner_list)
