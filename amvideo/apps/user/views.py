from rest_framework.generics import GenericAPIView
from amvideo.utils.myresponse import Myresponse
from . import ser
from amvideo.libs.tx_sms import send
from django.core.cache import cache
import re
from django.conf import settings
from . import models


# 账号密码登录接口
class LoginView(GenericAPIView):

    def post(self, request, *args, **kwargs):
        user_ser = ser.LoginSerializer(data=request.data)
        if user_ser.is_valid():
            username = user_ser.context['user'].username
            icon = user_ser.context['user'].icon
            token = user_ser.context['token']
            return Myresponse(username=username, token=token, icon=str(icon))
        return Myresponse(code=0, msg='失败', result=user_ser.errors)


#  短信验证码发送接口
class SendMsgView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        telephone = request.query_params.get('telephone')
        if re.match('^1[3-9][0-9]{9}$', telephone):
            code = send.get_code()
            cache.set(settings.PHONE_CACHE_KEY%telephone, code, 300)
            send.send_message(telephone, code)
            return Myresponse(result='验证码发送成功')
        else:
            return Myresponse(code=0, result='手机号格式不准确')


#  手机号验证接口
class CheckPhoneView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        telephone = request.query_params.get('telephone')
        user = models.User.objects.filter(telephone=telephone).first()
        if user:
            return Myresponse(result='用户存在')
        else:
            return Myresponse(code=0, msg='失败', result='用户不存在')


# 手机验证码登录接口
class CodeLoginView(GenericAPIView):

    def post(self, request, *args, **kwargs):
        code_ser = ser.CodeLoginSerializer(data=request.data)
        if code_ser.is_valid():
            username = code_ser.context['user'].username
            icon = code_ser.context['user'].icon
            token = code_ser.context['token']
            return Myresponse(username=username, token=token, icon=str(icon))
        else:
            return Myresponse(code=0, msg='失败', result=code_ser.errors)


# 注册接口
class RegisterView(GenericAPIView):

    def post(self, request, *args, **kwargs):
        register_ser = ser.RegisterSerializer(data=request.data)
        if register_ser.is_valid():
            register_ser.save()
            username = register_ser.context['username']
            token = register_ser.context['token']
            icon = register_ser.context['icon']
            return Myresponse(result='注册成功', username=username, token=token, icon=str(icon))
        else:
            return Myresponse(code=0, msg='失败', result=register_ser.errors)

