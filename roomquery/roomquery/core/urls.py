from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views
from .views import profile, PropertyCreateView, PropertyUpdateView, PropertyDeleteView
from .views import signup_view, login_view, logout_view, register, PropertyListView, PropertyDetailView
from .views import TenantBookingsView, book_property, booking_list ,landlord_bookings, respond_booking

urlpatterns = [
    path('', views.index, name='index'),
    #path('login/', views.login_view, name='login'),
    path('register/', register, name='register'),
    path('properties/', PropertyListView.as_view(), name='property_list'),
    path('property/<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail'),
    #path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logged_out.html'), name='logout'),
    path('signup/', signup_view, name='signup'),
    #path('login/', login_view, name='login'),
    #path('logout/', logout_view, name='logout'),
    path('', PropertyListView.as_view(), name='property_list'),
    path('profile/', profile, name='profile'),
    path('property/new/', PropertyCreateView.as_view(), name='property_create'),
    path('property/<int:pk>/edit/', PropertyUpdateView.as_view(), name='property_update'),
    path('property/<int:pk>/delete/', PropertyDeleteView.as_view(), name='property_delete'),
    path('property/<int:property_id>/book/', book_property, name='book_property'),
    path('bookings/', booking_list, name='booking_list'),
    path('property/<int:property_id>/book/', book_property, name='book_property'),
    path('bookings/', booking_list, name='booking_list'),
    path('landlord/bookings/', landlord_bookings, name='landlord_bookings'),
    path('landlord/bookings/<int:booking_id>/<str:response>/', respond_booking, name='respond_booking'),
    path('tenant/bookings/', TenantBookingsView.as_view(), name='tenant_bookings'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
