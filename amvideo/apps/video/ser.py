from . import models
from rest_framework import serializers
from django.db import transaction


# 视频分类接口序列化类
class VideoCategorySer(serializers.ModelSerializer):

    class Meta:
        model = models.VideoCategory
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {'read_only': True},
            'id': {'read_only': True},
        }


#  用户名称接口序列化类
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ['username']


#  视频群查接口序列化类
class VideoSerializer(serializers.ModelSerializer):

    user = UserSerializer()  # 重写字段， 用来获取外键字段的真实值
    # video_category = VideoCategorySer()

    class Meta:
        model = models.Video
        fields = ['id', 'video_img', 'video_link', 'brief',
                  'comment_num', 'duration', 'user', 'video_category']


#  视频评论获取序列化类
class VideoCommentGetSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = models.Comment
        fields = ['id', 'user', 'content', 'comment_time', 'get_son_comment']
        # extra_kwargs = {
        #     'id': {'read_only': True},
        #     'parent': {'write_only': True},
        #     'is_show': {'write_only': True},
        #     'get_son_comment': {'read_only': True},
        #     'video': {'write_only': True},
        #     'comment_time': {'read_only': True},
        #     'user': {'read_only': True},
        #     'user_id': {'write_only': True},
        # }

    # def validate(self, attrs):
    #     return attrs


#  视频评论发表序列化类
class VideoCommentSendSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        fields = ['user', 'content', 'parent', 'is_show', 'video', 'display_order']

    def create(self, validated_data):
        #  先将原始评论数从从对应的视频里面取出来
        old_num = models.Video.objects.filter(pk=validated_data.get('video').id)[0].comment_num
        # 使用数据库事务， 先将评论存入，然后再将原始评论数加1，更新视频对象的评论数量
        try:
            with transaction.atomic():
                comment = models.Comment.objects.create(**validated_data)
                old_num += 1
                models.Video.objects.filter(pk=comment.video.id).update(comment_num=old_num)
        except Exception as e:
            print(e)
        return comment

