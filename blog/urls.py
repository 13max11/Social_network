from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('like/<int:pk>', views.blog, name='entry-like'),
]