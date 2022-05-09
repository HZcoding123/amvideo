from rest_framework import serializers
from . import models
import re
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from django.core.cache import cache
from django.conf import settings


#  账号密码登录接口序列化类
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = models.User
        fields = ['username', 'password', 'icon', 'id']

        extra_kwargs = {
            'password': {'write_only': True},
            'icon': {'read_only': True},
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
                raise ValidationError('密码错误')
        else:
            raise ValidationError('用户名不存在')

    # 获取token
    def __get_token(self, user):
        # 通过user对象得到payload
        payload = jwt_payload_handler(user)
        # 通过payload获取到token
        token = jwt_encode_handler(payload)
        return token


#  手机验证码登录接口的序列化类
class CodeLoginSerializer(serializers.ModelSerializer):
    code = serializers.CharField()

    class Meta:
        model = models.User
        fields = ['telephone', 'code']

    # 全局钩子验证手机号和验证码
    def validate(self, attrs):
        user = self.__get_user(attrs)
        token = self.__get_token(user)
        self.context['user'] = user
        self.context['token'] = token
        return attrs

    # 通过手机号获取用户对象
    def __get_user(self, attrs):
        telephone = attrs.get('telephone')
        code = attrs.get('code')
        cache_code = cache.get(settings.PHONE_CACHE_KEY%telephone)
        if code == cache_code:
            user = models.User.objects.filter(telephone=telephone).first()
            if user:
                # 把完成认证之后的验证码删除
                cache.set(settings.PHONE_CACHE_KEY%telephone, '')
                return user
            else:
                raise ValidationError('该手机号不存在')
        else:
            raise ValidationError('验证码错误')

    # 通过用户对象获取token
    def __get_token(self, user):
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token


# 账号注册序列化类
class RegisterSerializer(serializers.ModelSerializer):
    code = serializers.CharField()

    class Meta:
        model = models.User
        fields = ['telephone', 'password', 'code']
        extra_kwargs = {
            'password': {
                'max_length': 128,
                'min_length': 8,
            }
        }

    # 全局钩子验证信息
    def validate(self, attrs):
        telephone = attrs.get('telephone')
        code = attrs.get('code')
        cache_code = cache.get(settings.PHONE_CACHE_KEY%telephone)
        if cache_code == code:
            user = models.User.objects.filter(telephone=telephone).first()
            if not user:
                # 在返回验证数据之前将用户名默认设置成手机号
                attrs['username'] = telephone
                # 在返回验证数据前将不属于数据库的数据pop出去
                attrs.pop('code')
                return attrs
            else:
                raise ValidationError('该用户已注册')
        else:
            raise ValidationError('验证码不正确')

    # 重写create方法将注册信息插入数据库
    def create(self, validated_data):
        # 验证后的信息打散插入数据库
        user = models.User.objects.create_user(**validated_data)
        # 获取token
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        # 将用户信息通过cntext属性传回给视图函数
        self.context['username'] = user.username
        self.context['icon'] = user.icon
        self.context['token'] = token
        return user

