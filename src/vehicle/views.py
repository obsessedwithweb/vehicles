from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Count
from datetime import datetime
import json
from .models import Blog, Services, Vehicle, Advertises
from checkout.models import Order, OrderItem



def home_page(request):
    template = 'vehicle/home.html'
    adv = Advertises.objects.all()
    services = Services.objects.all()
    blogs = Blog.objects.all()
    context = {
        'adv': adv,
        'services': services,
        'blogs': blogs,
    }
    return render(request, template, context)


class Cars(ListView):
    model = Vehicle
    template_name = 'vehicle/cars.html'
    context_object_name = "parts"

    def get_queryset(self):
        return Vehicle.objects.filter(type="car")


class Trucks(ListView):
    model = Vehicle
    template_name = 'vehicle/trucks.html'
    context_object_name = "parts"

    def get_queryset(self):
        return Vehicle.objects.filter(type="truck")


class Bicycles(ListView):
    model = Vehicle
    template_name = 'vehicle/bicycles.html'
    context_object_name = "parts"

    def get_queryset(self):
        return Vehicle.objects.filter(type="bicycle")

def vehicle_detail(request, vehicle_id):
    """Display a specific vehicle's details and allow adding to cart"""
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    
    # Check if we should show the cart sidebar (triggered by add_to_cart)
    show_cart = request.GET.get('show_cart') == 'true'
    
    context = {
        'vehicle': vehicle,
        'show_cart': show_cart
    }
    
    # If show_cart is True, add a script to toggle the cart when page loads
    if show_cart:
        context['custom_script'] = "document.addEventListener('DOMContentLoaded', function() { toggleCart(); });"
    
    return render(request, 'vehicle/detail.html', context)

@login_required
def dashboard(request):
    vehicles = Vehicle.objects.all()
    blogs = Blog.objects.all()
    services = Services.objects.all()
    adv = Advertises.objects.all()
    context = {
        'vehicles': vehicles,
        'blogs': blogs,
        'services': services,
        'adv': adv,
    }
    return render(request, 'vehicle/dashboard.html', context)

# Product Management Views
@login_required
def get_product(request, product_id):
    """API endpoint to get product details for editing"""
    try:
        product = Vehicle.objects.get(id=product_id)
        data = {
            'id': product.id,
            'name': product.name,
            'type': product.type,
            'price': product.price,
            'description': product.description,
            'image_url': product.image.url if product.image else None
        }
        return JsonResponse(data)
    except Vehicle.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
@require_POST
def add_product(request):
    """Add a new product"""
    try:
        name = request.POST.get('name')
        product_type = request.POST.get('type')
        price = request.POST.get('price')
        description = request.POST.get('description', '')
        
        if not all([name, product_type, price]):
            return JsonResponse({'success': False, 'message': 'Missing required fields'}, status=400)
        
        product = Vehicle(
            name=name,
            type=product_type,
            price=price,
            description=description
        )
        
        if 'image' in request.FILES:
            product.image = request.FILES['image']
            
        product.save()
        
        return JsonResponse({'success': True, 'message': 'Product added successfully', 'id': product.id})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
@require_POST
def edit_product(request, product_id):
    """Edit an existing product"""
    try:
        product = get_object_or_404(Vehicle, id=product_id)
        
        product.name = request.POST.get('name', product.name)
        product.type = request.POST.get('type', product.type)
        product.price = request.POST.get('price', product.price)
        product.description = request.POST.get('description', product.description)
        
        if 'image' in request.FILES:
            product.image = request.FILES['image']
            
        product.save()
        
        return JsonResponse({'success': True, 'message': 'Product updated successfully'})
    except Vehicle.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
@require_POST
def delete_product(request, product_id):
    """Delete a product"""
    try:
        product = get_object_or_404(Vehicle, id=product_id)
        product.delete()
        return JsonResponse({'success': True, 'message': 'Product deleted successfully'})
    except Vehicle.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
@require_POST
def change_password(request):
    """Handle password change requests"""
    try:
        data = json.loads(request.body)
        
        # Get the user's current form data
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        confirm_password = data.get('confirm_password', '')
        
        # Validate passwords match
        if new_password != confirm_password:
            return JsonResponse({'success': False, 'message': 'New passwords do not match'})
        
        # Use Django's built-in PasswordChangeForm for validation and security
        user = request.user
        form_data = {
            'old_password': current_password,
            'new_password1': new_password,
            'new_password2': confirm_password
        }
        
        form = PasswordChangeForm(user, form_data)
        
        if form.is_valid():
            # Save the form which changes the password
            user = form.save()
            
            # Update the session to prevent the user from being logged out
            update_session_auth_hash(request, user)
            
            return JsonResponse({
                'success': True,
                'message': 'Your password was successfully updated!'
            })
        else:
            # Extract error messages from the form
            errors = []
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(error)
            
            return JsonResponse({
                'success': False,
                'message': errors[0] if errors else 'Password change failed'
            })
            
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

# Advertisement Management Views
@login_required
def get_ad(request, ad_id):
    """API endpoint to get advertisement details for editing"""
    try:
        ad = Advertises.objects.get(id=ad_id)
        data = {
            'id': ad.id,
            'image_url': ad.image.url if ad.image else None
        }
        return JsonResponse(data)
    except Advertises.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Advertisement not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
@require_POST
def add_ad(request):
    """Add a new advertisement"""
    try:
        if 'image' not in request.FILES:
            return JsonResponse({'success': False, 'message': 'Image is required'}, status=400)
        
        ad = Advertises(image=request.FILES['image'])
        ad.save()
        
        return JsonResponse({'success': True, 'message': 'Advertisement added successfully', 'id': ad.id})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
@require_POST
def edit_ad(request, ad_id):
    """Edit an existing advertisement"""
    try:
        ad = get_object_or_404(Advertises, id=ad_id)
        
        if 'image' in request.FILES:
            ad.image = request.FILES['image']
            ad.save()
        
        return JsonResponse({'success': True, 'message': 'Advertisement updated successfully'})
    except Advertises.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Advertisement not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
@require_POST
def delete_ad(request, ad_id):
    """Delete an advertisement"""
    try:
        ad = get_object_or_404(Advertises, id=ad_id)
        ad.delete()
        return JsonResponse({'success': True, 'message': 'Advertisement deleted successfully'})
    except Advertises.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Advertisement not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

# Orders Management Views
@login_required
def get_orders(request):
    """API endpoint to get all orders"""
    try:
        orders = Order.objects.all().order_by('-created_at')
        orders_data = []
        
        for order in orders:
            orders_data.append({
                'id': order.id,
                'client_name': f"{order.first_name} {order.last_name}",
                'date': order.created_at.strftime('%Y-%m-%d %H:%M'),
                'total_amount': float(order.total_amount)
            })
        
        return JsonResponse({'orders': orders_data})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
def get_order_details(request, order_id):
    """API endpoint to get order details"""
    try:
        order = get_object_or_404(Order, id=order_id)
        order_items = OrderItem.objects.filter(order=order).select_related('product')
        
        items_data = []
        for item in order_items:
            items_data.append({
                'product_id': item.product.id,
                'product_name': item.product.name,
                'price': float(item.price),
                'quantity': item.quantity
            })
        
        order_data = {
            'id': order.id,
            'client_name': f"{order.first_name} {order.last_name}",
            'phone': order.phone,
            'address': f"{order.wilaya}, {order.daira}, {order.address}",
            'email': order.email,
            'date': order.created_at.strftime('%Y-%m-%d %H:%M'),
            'total_amount': float(order.total_amount),
            'notes': order.notes,
            'items': items_data
        }
        
        return JsonResponse(order_data)
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Order not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

# Clients Management Views
@login_required
def get_clients(request):
    """API endpoint to get client information"""
    try:
        # Get all unique customers from orders
        orders = Order.objects.all()
        
        # Create a dictionary of clients with their order counts
        clients = {}
        
        for order in orders:
            client_key = f"{order.first_name}_{order.last_name}_{order.phone}"
            if client_key not in clients:
                clients[client_key] = {
                    'id': order.id,  # Using first order ID as client ID
                    'name': f"{order.first_name} {order.last_name}",
                    'phone': order.phone,
                    'email': order.email,
                    'order_count': 0,
                    'cart_count': 0  # We don't track this yet
                }
            
            clients[client_key]['order_count'] += 1
        
        # Convert to list for JSON response
        clients_list = list(clients.values())
        
        return JsonResponse({'clients': clients_list})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


class SearchView(ListView):
    model = Vehicle
    template_name = "vehicle/search.html"
    context_object_name = "parts"

    def get_queryset(self):
        query = self.request.GET.get('search')
        parts = Vehicle.objects.filter(name__icontains=query)
        return parts
