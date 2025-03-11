from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='auth_sys/login.html', redirect_authenticated_user=True), name='login'),
    path('register/', views.registration, name='register'),
    path('logout/', views.logout_view, name='logout'),
]