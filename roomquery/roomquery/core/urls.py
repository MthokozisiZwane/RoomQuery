from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('properties/', views.PropertyListView.as_view(), name='property_list'),
    path('property/<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail'),
]
