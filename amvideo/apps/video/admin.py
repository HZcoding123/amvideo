from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Video)
admin.site.register(models.VideoCategory)
admin.site.register(models.Comment)