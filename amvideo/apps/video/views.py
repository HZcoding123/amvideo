from rest_framework.generics import GenericAPIView
from . import ser
from . import models
from amvideo.utils.myresponse import Myresponse
from django.core.cache import cache
from celery_task.category import video_category
from .paginations import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from celery_task.saveComment import save_comment
from amvideo.utils.throttings import CommentThrotting
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.serializers import jwt_decode_handler



'''
视频分类接口
1.先从redis里面取出来
2.判断redis是否存在数据
3.如果不存在数据就celery异步加载到redis里面去
'''
class VideoCategory(GenericAPIView):

    def get(self, request, *args, **kwargs):
        category_list = cache.get('video_category')
        if not category_list:
            video_category().delay()
            category_list = cache.get('video_category')
        return Myresponse(data=category_list)


# 视频群查接口
class VideoView(GenericAPIView):
    queryset = models.Video.objects.filter(is_delete=False, is_show=True).order_by('display_order')
    serializer_class = ser.VideoSerializer
    pagination_class = PageNumberPagination  # 指定分页器
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]  # 普通字段的过滤

    filter_fields = ['video_category']  # 根据什么字段过滤
    # search_fields = ['name']  # 使用自带的search过滤方法可以过滤字段的部分文字匹配 ?search=xxx
    # ordering_fields = ['id']  # 根据什么字段排序  倒叙加上-号

    def get(self, request, *args, **kwargs):
        video_list = cache.get('video_list')  # 先从缓存里面取
        if not video_list:  # 如果缓存里面没有
            video_list = self.get_queryset()  # 获取所有视频
            cache.set('video_list', video_list, 60*60*24)  # 存入到缓存
        video_list = self.filter_queryset(video_list)  # 先按照字段过滤
        page_list = self.paginate_queryset(video_list)  # 将过滤后的结果进行分页操作
        video_data = self.get_serializer(page_list, many=True)  # 分页结果进行序列化
        count_res = video_list.count()/self.pagination_class.page_size  # 按照f分页大小数据计算总的页数
        total_pages = int(count_res) + 1 if count_res - int(count_res) > 0 else int(count_res)  # 三目运算解决页数小数情况
        return Myresponse(data=video_data.data, total_num=total_pages)


# 发表评论接口
class CommentSaveView(GenericAPIView):

    # 限制评论发表接口的访问评率
    throttle_classes = [CommentThrotting]

    # token鉴权，验证前端用户是否登录状态（前端请求时是否携带token过来，或者携带的token是否过期）
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    '''
        评论存储视图，通过celery异步处理，存入数据库
    '''
    def post(self, request, *args, **kwargs):
        request_token = request.headers['Authorization']  # 根据前端的请求头取出token
        user_id = jwt_decode_handler(request_token[4:])['user_id']  # 使用登录用户的token反向解析出用户对象
        request.data['user'] = user_id   # 给前端请求体的评论信息加上用户id方便序列化存入数据库
        print(request.data)
        # save_comment.delay(request.data)  # 将需要存储的评论信息交给celery异步存储
        return Myresponse(result='成功')


# 评论获取接口
class CommentGetView(GenericAPIView):

    queryset = models.Comment.objects.filter(is_delete=False, is_show=True).order_by('display_order')
    serializer_class = ser.VideoCommentGetSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]  # 普通字段的过滤

    filter_fields = ['video']  # 设置get请求写携带的过滤参数

    '''
        评论获取视图，get请求
    '''
    def get(self, request, *args, **kwargs):
        # 先从缓存里面取
        comment_list = cache.get('comment_list')
        if not comment_list:
            comment_list = self.get_queryset()
            cache.set('comment_list', comment_list, 60*60*24)
        comment_list = self.filter_queryset(comment_list)  # 按照get请求过滤字段过滤
        comment_data = self.get_serializer(comment_list, many=True)  # 按照过滤结果进行序列化
        print(comment_data.data)
        return Myresponse(data=comment_data.data)
