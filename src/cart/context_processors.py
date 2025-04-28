# context_processors.py
from .models import Cart, CartItem

def session_processor(request):
    """Make session ID available in all templates"""
    return {
        'custom_session_id': getattr(request, 'custom_session_id', None)
    }

def cart_processor(request):
    """Make cart information available in all templates"""
    
    if hasattr(request, 'custom_session_id'):
        try:
            cart = Cart.objects.get(session_id=request.custom_session_id)
            cart_items = CartItem.objects.filter(cart=cart).select_related('product')
            
            return {
                'custom_session_id': request.custom_session_id,
                'cart': cart,
                'cart_items': cart_items,
                'cart_total_quantity': cart.total_quantity,
                'cart_total_price': cart.total_pricing
            }
        except Cart.DoesNotExist:
            pass
    
    # Return default values if no cart exists
    return {
        'custom_session_id': getattr(request, 'custom_session_id', None),
        'cart_total_quantity': 0,
        'cart_total_price': 0,
        'cart_items': []
    }