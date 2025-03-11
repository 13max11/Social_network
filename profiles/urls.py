from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('history/', views.history, name='history'),
    path('', views.my_profil, name='my_profile'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/posts/', views.posted, name='profile-posts'),
    path('<str:username>/comments/', views.commented, name='profile-commented'),
    path('<str:username>/liked/', views.liked, name='profile-liked'),
    path('<str:username>/groups/<slug:slug>', views.community_group, name='community_group'),
]