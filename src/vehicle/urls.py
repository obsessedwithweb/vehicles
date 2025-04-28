from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('cars/', views.Cars.as_view(), name='cars-parts'),
    path('trucks/', views.Trucks.as_view(), name='trucks-parts'),
    path('bicycles/', views.Bicycles.as_view(), name='bicycles-parts'),
    path('vehicle/<int:vehicle_id>/', views.vehicle_detail, name='vehicle-detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Product Management URLs
    path('vehicle/get/<int:product_id>/', views.get_product, name='get-product'),
    path('vehicle/add/', views.add_product, name='add-product'),
    path('vehicle/edit/<int:product_id>/', views.edit_product, name='edit-product'),
    path('vehicle/delete/<int:product_id>/', views.delete_product, name='delete-product'),
    
    # Advertisement Management URLs
    path('vehicle/ad/get/<int:ad_id>/', views.get_ad, name='get-ad'),
    path('vehicle/ad/add/', views.add_ad, name='add-ad'),
    path('vehicle/ad/edit/<int:ad_id>/', views.edit_ad, name='edit-ad'),
    path('vehicle/ad/delete/<int:ad_id>/', views.delete_ad, name='delete-ad'),
    
    # Orders and Clients Management URLs
    path('vehicle/orders/', views.get_orders, name='get-orders'),
    path('vehicle/order/<int:order_id>/', views.get_order_details, name='get-order-details'),
    path('vehicle/clients/', views.get_clients, name='get-clients'),
    
    # User Account Management
    path('change-password/', views.change_password, name='change-password'),
]
