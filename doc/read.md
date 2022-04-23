# 开发流程:

# 一.项目目录调整

1.`二级根目录下建立apps包, logs文件夹, scripts文件夹`

2.`二级根目录下建立settings包, libs包`

3.`settings包下建立dev，pro py文件用于开发和上线的配置`

4.`复制原来settings文件里面内容到dev文件里面，同时更改manage.py以及wsgi文件里面的配置`

5.`通过python manage.py run server启动服务，同时将Edit config里面环境变量修改为DJANGO_SETTINGS_MODULE=amvideo.settings.dev方便快速启动服务`

6.`配置文件做国际化处理，并且添加app`

7.`注册app，注册之前需要将二级根目录添加到环境变量(sys.path.insert(0, BASE_DIR)), 然后将apps文件夹也添加到环境变量(sys.path.insert(1, os.path.join(BASE_DIR, 'apps'')))`

8.`注册完成之后将apps文件夹设置为source root，这样导入文件的时候不会报错`

