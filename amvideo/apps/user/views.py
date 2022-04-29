from rest_framework.generics import GenericAPIView
from amvideo.utils.myresponse import Myresponse
from . import ser


# 账号密码登录接口
class LoginView(GenericAPIView):

    def post(self, request, *args, **kwargs):
        user_ser = ser.LoginSerializer(data=request.data)
        if user_ser.is_valid():
            username = user_ser.context['user'].username
            token = user_ser.context['token']
            return Myresponse(username=username, token=token)
        return Myresponse(code=0, msg='失败', result=user_ser.errors)

