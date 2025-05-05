from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('upload_skincolor/', views.upload_skincolor, name='upload_skincolor'),
    path('upload_clothing/', views.upload_clothing, name='upload_clothing'),
    path('clothing_list/', views.clothing_list, name='clothing_list'),
]