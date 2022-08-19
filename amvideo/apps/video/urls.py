from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.VideoCategory.as_view()),
    path('all/', views.VideoView.as_view()),
    path('savecomment/', views.CommentSaveView.as_view()),
    path('getcomment/', views.CommentGetView.as_view()),
]
