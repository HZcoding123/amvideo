from rest_framework.generics import GenericAPIView
from amvideo.utils.myresponse import Myresponse


class test(GenericAPIView):
    def get(self, request, *args, **kwargs):
        dic = {'name': 'william'}
        return Myresponse(code=0,result=dic)