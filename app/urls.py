from django.urls import path, re_path

from django.contrib.auth import views as auth_views

from django.views.generic import TemplateView       # Need to import inorder to load the template directly without using the help of views.py


from . import views
# from .views import loginPage, clientregisterPage, home, activate



## All app urls here ...


urlpatterns = [

    path('', views.home, name="home"),


    path('login/', views.loginPage, name="login"),


    path('register/', views.clientregisterPage, name="register"),


    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]


