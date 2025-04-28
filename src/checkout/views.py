from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.db import transaction

from cart.models import Cart, CartItem
from .models import Order, OrderItem

def checkout_view(request):
    """Display checkout page with cart items"""
    session_id = request.custom_session_id
    
    # Optimized query using select_related to reduce database hits
    cart_items = CartItem.objects.filter(
        cart__session_id=session_id
    ).select_related('product', 'cart')
    
    # If no cart items exist, redirect to cart page
    if not cart_items.exists():
        return redirect('cart:view_cart')
    
    # Get the cart from the first cart item to avoid an extra query
    cart = cart_items.first().cart if cart_items else None
    
    # Get wilaya choices from the model
    wilaya_choices = Order.WilayaChoices.choices
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'wilaya_choices': wilaya_choices,
    }
    
    return render(request, 'checkout/checkout.html', context)

@require_POST
@transaction.atomic
def process_order(request):
    """Process the checkout form and create an order"""
    # Optimized query for cart items
    cart_items = CartItem.objects.filter(
        cart__session_id=request.custom_session_id
    ).select_related('product', 'cart')
    
    # If no items, redirect back to cart
    if not cart_items.exists():
        return redirect('cart:view_cart')
    
    # Get cart from the first item
    cart = cart_items.first().cart
    
    # Get form data
    first_name = request.POST.get('firstName')
    last_name = request.POST.get('lastName')
    phone = request.POST.get('phone')
    wilaya = request.POST.get('wilaya')
    daira = request.POST.get('daira')
    address = request.POST.get('address', '')
    email = request.POST.get('email', '')
    notes = request.POST.get('notes', '')
    
    # Validate required fields
    if not all([first_name, last_name, phone, wilaya, daira]):
        return redirect('checkout:checkout')
    
    # Create order
    order = Order.objects.create(
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        wilaya=wilaya,
        daira=daira,
        address=address,
        email=email,
        notes=notes,
        total_amount=cart.total_pricing,
        session_id=cart.session_id
    )
    
    # Create order items
    order_items = []
    for item in cart_items:
        order_items.append(OrderItem(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        ))
    # Bulk create for better performance
    OrderItem.objects.bulk_create(order_items)
    
    # Clear cart
    cart_items.delete()
    cart.total_quantity = 0
    cart.total_pricing = 0
    cart.save()
    
    # Redirect to success page
    return redirect('checkout:order_success', order_id=order.id)

def order_success(request, order_id):
    """Display order success page"""
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order).select_related('product')
    
    context = {
        'order': order,
        'order_items': order_items
    }
    
    return render(request, 'checkout/success.html', context)
