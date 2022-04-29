from rest_framework import serializers
from . import models
import re
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler


#  账号密码登录接口序列化类
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = models.User
        fields = ['username', 'password', 'id']

        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
        }

    # 全局钩子验证前端传过来的账号密码
    def validate(self, attrs):
        user = self.__get_user(attrs)
        token = self.__get_token(user)
        self.context['user'] = user
        self.context['token'] = token
        return attrs

    # 获取用户对象
    def __get_user(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        # 多种登录方式
        # 1.手机号
        if re.match('^1[3-9][0-9]{9}$', username):
            user = models.User.objects.filter(telephone=username).first()
        elif re.match('^[0-9a-zA-Z.]+@[0-9a-zA-Z.]+?com$', username):
            user = models.User.objects.filter(email=username).first()
        else:
            user = models.User.objects.filter(username=username).first()
        if user:
            res = user.check_password(password)
            if res:
                return user
            else:
                return ValidationError('密码错误')
        else:
            return ValidationError('用户名不存在')

    # 获取token
    def __get_token(self, user):
        # 通过user对象得到payload
        payload = jwt_payload_handler(user)
        # 通过payload获取到token
        token = jwt_encode_handler(payload)
        return token


