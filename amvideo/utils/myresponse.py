from rest_framework.response import Response


# 自定义返回对象
class Myresponse(Response):

    def __init__(self, code=100, msg='成功', status=None, result=None,
                 headers=None, content_type=None,**kwargs):
        dic = {'code': code,
               'msg': msg
               }
        if result:
            dic['result'] = result
        dic.update(kwargs)
        super().__init__(data=dic, status=status, headers=headers, content_type=content_type)