from rest_framework.throttling import SimpleRateThrottle


class SMSThrotting(SimpleRateThrottle):
    scope = 'sms'

    def get_cache_key(self, request, view):
        # 根据ip来限制普通接口的访问次数
        # return self.get_ident(request)
        # 根据get请求的参数来限制, 不同参数就是不同的请求个体
        phone = request.query_params.get('telephone')
        return self.cache_format%{'scope': self.scope, 'ident': phone}


class CommentThrotting(SimpleRateThrottle):

    scope = 'comment'

    def get_cache_key(self, request, view):   # 根据ip地址限制评论次数
        return self.get_ident(request)


