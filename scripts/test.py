import requests
import os
import re
from PIL import Image

#  科技
'''
https://video.pearvideo.com/mp4/short/20220404/cont-1757471-15856034-hd.mp4
https://video.pearvideo.com/mp4/short/20220404/cont-1757458-15855964-hd.mp4
https://video.pearvideo.com/mp4/short/20220404/cont-1757464-15855994-hd.mp4
https://video.pearvideo.com/mp4/short/20220404/cont-1757442-15855880-hd.mp4
https://video.pearvideo.com/mp4/short/20220404/cont-1757435-15855849-hd.mp4
'''

#  汽车
'''
https://video.pearvideo.com/mp4/short/20220520/cont-1762844-15882984-hd.mp4
https://video.pearvideo.com/mp4/adshort/20220520/cont-1762821-15882853_adpkg-ad_hd.mp4
https://video.pearvideo.com/mp4/adshort/20220516/cont-1762349-15880341_adpkg-ad_hd.mp4
https://video.pearvideo.com/mp4/short/20220404/cont-1757442-15855880-hd.mp4
https://video.pearvideo.com/mp4/short/20220404/cont-1757435-15855849-hd.mp4
'''
# https://www.pearvideo.com/category_loading.jsp?reqType=5&categoryId=6&start=24
# # 往目标网址发送请求
# video_data = requests.get('https://www.pearvideo.com/category_loading.jsp?reqType=5&categoryId=6&start=36')
#
# # 正则匹配网址中的图片地址
# res = re.findall('background-image: url(.*?);', video_data.text)
#
# # 拼接桌面路径
# desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
#
# # 拼接目标文件路径
# file = os.path.join(desktop, 'amvideo_source')
#
# # for循环遍历所有的图片地址
# a = 26
# for r in res:
#     img_data = requests.get(r[1:-1])
#     with open(file+str(a)+'.png', 'wb') as f:
#         for data in img_data.iter_content():
#             f.write(data)
#     a += 1


"""
修改图片尺寸
"""
# 原始图片路径
# file_path = os.path.join(os.path.join(os.path.expanduser('~'), 'Desktop'), 'amvideo_source')
#
# # 遍历所有的图像
# raw_file = os.walk(file_path)
#
# # 修改后图片尺寸大小
# width, height = 242, 200
#
# # 修改后程序存储的路径
# save_path = os.path.join(os.path.join(os.path.expanduser('~'), 'Desktop'), 'amvideo_img')
#
# for root, dirs, files, in raw_file:
#     for file in files:  # 遍历得到每个图片的名字
#         if not file == '.DS_Store':
#             picture_path = os.path.join(root, file)  # 拼接原始图片的绝对路径
#             pic_org = Image.open(picture_path)  # 打开图片
#             pic_new = pic_org.resize((width, height), Image.ANTIALIAS)   # 图像尺寸修改
#             pic_new_path = os.path.join(save_path, file)  # 新图像存储绝对路径
#             pic_new.save(pic_new_path)  # 把设置好的图片存到新的文件路径中









