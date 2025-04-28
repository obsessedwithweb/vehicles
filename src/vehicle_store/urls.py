from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import RedirectView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

# Simple redirect view
def redirect_to_login(request):
    return HttpResponseRedirect('/accounts/login/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vehicle.urls')),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls')),
    
    # Disable unwanted allauth paths by redirecting them
    path('accounts/signup/', redirect_to_login),
    path('accounts/password/reset/', redirect_to_login),
    path('accounts/password/change/', redirect_to_login),
    path('accounts/confirm-email/', redirect_to_login),
    path('accounts/password/set/', redirect_to_login),
    path('accounts/inactive/', redirect_to_login),
    path('accounts/email/', redirect_to_login),
    path('accounts/social/', redirect_to_login),
    path('accounts/connections/', redirect_to_login),
    
    # Include only the login and logout URLs
    path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
