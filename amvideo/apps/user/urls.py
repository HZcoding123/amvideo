from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('send/', views.SendMsgView.as_view()),
    path('check/', views.CheckPhoneView.as_view()),
    path('code/', views.CodeLoginView.as_view()),
    path('register/', views.RegisterView.as_view()),
]
