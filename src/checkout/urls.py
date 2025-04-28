from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout_view, name='checkout'),
    path('process/', views.process_order, name='process_order'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
]
