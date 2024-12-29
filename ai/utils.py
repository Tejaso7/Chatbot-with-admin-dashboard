import uuid
import json
import requests
from django.utils.timezone import now, timedelta
from .models import Session

def get_client_ip(request):
    """Get the client IP address from the request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_location_from_ip(ip):
    """Fetch location data based on IP address using a geolocation API."""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        if response.status_code == 200:
            data = response.json()
            return {
                "country": data.get("country", "Unknown"),
                "region": data.get("regionName", "Unknown"),
                "city": data.get("city", "Unknown"),
                "lat": data.get("lat"),
                "lon": data.get("lon")
            }
    except Exception as e:
        print(f"Error fetching location data: {e}")
    return {"country": "Unknown", "region": "Unknown", "city": "Unknown", "lat": None, "lon": None}

def create_or_validate_session(request):
    session_id = request.COOKIES.get('session_id')
    user_agent = request.META.get('HTTP_USER_AGENT', '')  # Get the user agent
    client_ip = get_client_ip(request)  # Get the client IP address

    if session_id:
        try:
            # Validate existing session
            session = Session.objects.get(session_id=session_id, is_valid=True)
            
            # Check if the IP and user agent match
            if session.client_ip == client_ip and session.user_agent == user_agent:
                return session  # Session is valid for this browser

            # Invalidate the session if details don't match
            session.is_valid = False
            session.save()
        except Session.DoesNotExist:
            pass  # Proceed to create a new session if validation fails

    # Create a new session if validation fails or no session exists
    new_session_id = str(uuid.uuid4())
    location_data = get_location_from_ip(client_ip)
    created_at = now()
    expired_at = created_at + timedelta(hours=1)

    # Create session in the database
    session = Session.objects.create(
        session_id=new_session_id,
        client_ip=client_ip,
        user_agent=user_agent,
        location_country=location_data.get("country"),
        location_region=location_data.get("region"),
        location_city=location_data.get("city"),
        location_lat=location_data.get("lat"),
        location_lon=location_data.get("lon"),
        session_data=json.dumps({"message_history": []}),  # Example data
        created_at=created_at,
        expired_at=expired_at,
        is_valid=True
    )

    return session


 