from django.urls import path
from . import views



urlpatterns = [
    path('register/', views.register, name='register'),
    path('activate/', views.activate, name='activate'),
    path('success/', views.success, name='success'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]