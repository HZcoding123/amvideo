from video import models
from video import ser
from .celery import app
from django.core.cache import cache


# celery异步加载分类数据
@app.task
def video_category():
    category_celery_list = models.VideoCategory.objects.filter(is_delete=False, is_show=True).order_by('display_order')
    category_celery_ser = ser.VideoCategorySer(category_celery_list, many=True)
    cache.set('video_category', category_celery_ser.data, 60*60*24)
    return True
