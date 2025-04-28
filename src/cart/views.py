from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect

from .models import Cart, CartItem
from vehicle.models import Vehicle

def get_cart(request):
    """Get or create cart for the current session"""
    try:
        cart = Cart.objects.get(session_id=request.custom_session_id)
    except Cart.DoesNotExist:
        # This should not happen due to middleware, but just in case
        cart = Cart.objects.create(session_id=request.custom_session_id)
    return cart

@require_POST
def add_to_cart(request):
    """Add a product to cart"""
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url') or request.META.get('HTTP_REFERER', reverse('home'))
    
    if not product_id:
        return HttpResponseRedirect(redirect_url)
    
    if quantity <= 0:
        return HttpResponseRedirect(redirect_url)
    
    # Get product
    try:
        product = Vehicle.objects.get(id=product_id)
    except Vehicle.DoesNotExist:
        return HttpResponseRedirect(redirect_url)
        
    cart = get_cart(request)
    
    # Add to cart
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += quantity
        cart_item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(cart=cart, product=product, quantity=quantity)

    # Toggle cart sidebar if requested
    if request.POST.get('show_cart') == 'true':
        # Add a fragment to trigger the cart sidebar
        if '?' in redirect_url:
            redirect_url += '&show_cart=true'
        else:
            redirect_url += '?show_cart=true'
    
    # Redirect back
    return HttpResponseRedirect(redirect_url)

@require_POST
def remove_from_cart(request):
    """Remove an item from cart"""
    product_id = request.POST.get('product_id')
    redirect_url = request.POST.get('redirect_url') or request.META.get('HTTP_REFERER', reverse('home'))
    
    if not product_id:
        return HttpResponseRedirect(redirect_url)
    
    # Get cart and product
    cart = get_cart(request)
    
    try:
        product = Vehicle.objects.get(id=product_id)
    except Vehicle.DoesNotExist:
        return HttpResponseRedirect(redirect_url)
    
    # Remove from cart
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        # Update cart totals after deletion
        cart.update_totals()
    except CartItem.DoesNotExist:
        pass
        # ndir loggin hna

    return HttpResponseRedirect(redirect_url)

@require_POST
def update_cart(request):
    """Update item quantity"""
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 0))
    redirect_url = request.POST.get('redirect_url') or request.META.get('HTTP_REFERER', reverse('home'))
    
    if not product_id:
        return HttpResponseRedirect(redirect_url)
    
    # Get cart and product
    cart = get_cart(request)
    
    try:
        product = Vehicle.objects.get(id=product_id)
    except Vehicle.DoesNotExist:
        return HttpResponseRedirect(redirect_url)
    
    # Update or remove
    if quantity <= 0:
        # Remove item if quantity is zero or negative
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.delete()
            # Update cart totals after deletion
            cart.update_totals()
        except CartItem.DoesNotExist:
            pass
            # messages.info(request, "That item is not in your cart.")
    else:
        # Update quantity
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity = quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            # If the item doesn't exist, create it
            CartItem.objects.create(cart=cart, product=product, quantity=quantity)

    return HttpResponseRedirect(redirect_url)

def view_cart(request):
    """View cart contents"""
    cart = get_cart(request)
    cart_items = CartItem.objects.filter(cart=cart).select_related('product')
    
    context = {
        'cart': cart,
        'cart_items': cart_items
    }
    
    return render(request, 'cart/cart.html', context)

@require_POST
def clear_cart(request):
    """Clear all items from cart"""
    redirect_url = request.POST.get('redirect_url') or request.META.get('HTTP_REFERER', reverse('home'))
    
    cart = get_cart(request)
    CartItem.objects.filter(cart=cart).delete()
    cart.total_quantity = 0
    cart.total_pricing = 0
    cart.save()
    
    return HttpResponseRedirect(redirect_url)
