from video import ser
from video import models
from .celery import app


@app.task
def save_comment(request_data):
    comment_ser = ser.VideoCommentSendSerializer(data=request_data)   # 先将请求的数据反序列化
    if comment_ser.is_valid(raise_exception=True):  # 判断存入
        comment_ser.save()
    return True



































































































































































































































































