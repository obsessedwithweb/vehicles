# middleware.py
import uuid6
from django.utils.deprecation import MiddlewareMixin
from .models import Cart

class CustomSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check for existing session key
        if not request.session.session_key:
            # Force session creation
            request.session.create()
            
            # Create a UUID7 (time-ordered UUID)
            custom_session_id = str(uuid6.uuid7())
            
            # Store UUID7 in session
            request.session['custom_session_id'] = custom_session_id
            
            # Create cart for this session
            Cart.objects.create(session_id=custom_session_id)
        else:
            # Get existing custom_session_id or create one if missing
            custom_session_id = request.session.get('custom_session_id')
            if not custom_session_id:
                custom_session_id = str(uuid6.uuid7())
                request.session['custom_session_id'] = custom_session_id
                Cart.objects.create(session_id=custom_session_id)
                
        # Make the custom_session_id available directly on the request object
        request.custom_session_id = request.session.get('custom_session_id')
        
    def process_response(self, request, response):
        # Ensure session is saved
        if hasattr(request, 'session') and request.session.modified:
            request.session.save()
        return response