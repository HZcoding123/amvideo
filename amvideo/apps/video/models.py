from amvideo.utils.basemodel import BaseModel
from django.db import models
from user.models import User
# Create your models here.


# 视频表
class Video(BaseModel):
    name = models.CharField(max_length=128, verbose_name='视频名称')
    video_img = models.ImageField(upload_to='video', verbose_name='封面图片', blank=True, null=True)
    video_link = models.CharField(max_length=255, null=True, blank=True, verbose_name='视频链接')
    brief = models.CharField(max_length=2048, null=True, blank=True, verbose_name='视频简介')
    comment_num = models.BigIntegerField(verbose_name='评论数量', default=0)
    duration = models.CharField(max_length=128, verbose_name='视频时长', null=True, blank=True)

    # 关联字段 与分类一对多
    video_category = models.ForeignKey('VideoCategory', on_delete=models.SET_NULL, related_name='video',
                                       db_constraint=False, null=True, blank=True, verbose_name='视频分类')
    # 关联字段 与用户一对多
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='video', db_constraint=False,
                             null=True, blank=True, verbose_name='视频用户')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 分类表
class VideoCategory(BaseModel):

    name = models.CharField(max_length=255, verbose_name='分类名称', unique=True)

    class Meta:
        verbose_name = '视频分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 评论表
class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论用户', related_name='user_comment')
    video = models.ForeignKey('Video', on_delete=models.CASCADE, verbose_name='评论视频', related_name='video_comment')
    content = models.CharField(max_length=255, verbose_name='评论内容')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='son_comment')  # 自关联，子评论

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    @property
    def get_son_comment(self):  # 将评论的子评论返回,子评论是一个一个的对象，需要通过遍历的方式将对象的一个一个字段返回
        son_comment_list = []
        for son in self.son_comment.all():
            son_comment_list.append({
                "user": {
                    "username": son.user.username,
                    "icon": str(son.user.icon)
                },
                "content": son.content,
                "comment_time": son.comment_time,
            })
        return son_comment_list

    def __str__(self):
        return self.content





