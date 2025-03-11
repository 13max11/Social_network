from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>/', views.community_details_view, name='community'),
    path('<slug:slug>/<int:pk>/', views.post_details_view, name='post'),
    path('create/post/', views.post_create, name='post-create'),
    path('create/community/', views.community_create, name='community-create'),
    path('explore', views.explore, name='explore'),
    path('rules', TemplateView.as_view(template_name='auth_sys/rules.html'), name='rules'),
]