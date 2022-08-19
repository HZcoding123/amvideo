import os
import django
from celery import Celery

# 加载django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amvideo.settings.dev')
django.setup()

broker = 'redis://127.0.0.1:6379/1'  # 任务队列

backend = 'redis://127.0.0.1:6379/2'  # 结果存储，执行完的结果存储在这里

app = Celery(__name__, broker=broker, backend=backend, include=['celery_task.banner', 'celery_task.category', 'celery_task.saveComment'])

#  celery --app=celery_task worker -l INFO  启动worker


