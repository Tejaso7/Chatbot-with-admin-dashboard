from django.utils.deprecation import MiddlewareMixin
from .models import Session

class ValidateSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        session_id = request.COOKIES.get('session_id')
        if session_id:
            try:
                # Fetch and validate the session from the database
                session = Session.objects.get(session_id=session_id, is_valid=True)
                request.session_obj = session  # Attach session to the request object
            except Session.DoesNotExist:
                request.session_obj = None
        else:
            request.session_obj = None
