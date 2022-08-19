from .celery import app
from home import models
from home import ser
from django.core.cache import cache
from django.conf import settings


@app.task
def banner_update():
    banner_category_list = models.Banner.objects.filter(is_delete=False, is_show=True).order_by('display_order')[:settings.BANNER_COUNTING]
    banner_category_ser = ser.BannerViewSerializer(banner_category_list, many=True)

    for banner in banner_category_ser.data:
        banner['img'] = 'http://127.0.0.1:8000' + banner['img']
    cache.set('banner_list', banner_category_ser.data, 60*60*24)
    return True