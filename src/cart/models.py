from django.db import models
from vehicle.models import Vehicle


# Create your models here.
# models.py
from django.db import models
from django.contrib.sessions.models import Session

class Cart(models.Model):
    session_id = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_quantity = models.PositiveIntegerField(default=0)
    total_pricing = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Cart {self.session_id}"
    
    def update_totals(self):
        """Update cart totals based on its items"""
        items = self.items.all()
        self.total_quantity = sum(item.quantity for item in items)
        self.total_pricing = sum(item.product.price * item.quantity for item in items)
        self.save()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('cart', 'product')
        
    def __str__(self):
        return f"{self.quantity} × {self.product.name}"
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update cart totals when an item is saved
        self.cart.update_totals()