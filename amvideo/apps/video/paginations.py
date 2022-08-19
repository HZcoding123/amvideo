from rest_framework.pagination import PageNumberPagination as MyPageNumberPagination

'''
自定义分页类
'''


class PageNumberPagination(MyPageNumberPagination):
    page_size = 12  # 一页多少个数据
    page_query_param = 'page'  # 获取前端传过来的页码数
    # max_page_size = 10  # 最大的页码
    page_size_query_param = page_size  # 默认每页显示12个
