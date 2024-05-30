from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import signup_view, login_view, logout_view, PropertyListView, PropertyDetailView

urlpatterns = [
    path('', views.index, name='index'),
    #path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('properties/', views.PropertyListView.as_view(), name='property_list'),
    path('property/<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail'),
    #path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(template_name='logged_out.html'), name='logout'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
