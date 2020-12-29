from django.urls import path
from hw7 import views

app_name = 'hw7'

urlpatterns = [
    path('', views.login),
    path('register/', views.register),
    path('home/', views.home),
    path('login/', views.login),
    path('logout/', views.logout),
    path('getCode/', views.getCode, name='getCode'),
]