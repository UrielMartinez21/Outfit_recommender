from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('skincolor/', views.skincolor, name='skincolor'),
    path('facephoto_delete/<int:id>/', views.facephoto_delete, name='facephoto_delete'),

    path('clothing/', views.clothing, name='clothing'),
    path('clothing_list/<int:id>/delete/', views.clothing_delete, name='clothing_delete'),

    # recommender
    path('recommender/', views.recommender, name='recommender'),
]