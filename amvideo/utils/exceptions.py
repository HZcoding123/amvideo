from rest_framework.views import exception_handler
from .myresponse import Myresponse


# 自定义异常捕获的对象
def common_excepeion_handler(exc, context):
    ret = exception_handler(exc, context)
    if not ret:  # 如果rest_framework处理不了， 就让django自己来处理
        return Myresponse(code=0, msg='失败', result=str(exc))
    else:
        return Myresponse(code=0, msg='失败', result=ret.data)


