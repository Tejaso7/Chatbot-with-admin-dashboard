from django.db import models
from django.utils.timezone import localtime , now
from pytz import timezone

def get_current_ist_time():
    # Convert UTC to IST using pytz
    ist_timezone = timezone('Asia/Kolkata')
    current_time = localtime(now(), ist_timezone)
    return current_time

from django.db import models
from django.utils.timezone import now, timedelta 
from datetime import timedelta
from django.utils.timezone import now
from datetime import timedelta

def default_expiration_time():
    return now() + timedelta(hours=1)


class Session(models.Model):
    session_id = models.CharField(max_length=255, unique=True, default="default_session_id")  # Unique session ID
    client_ip = models.CharField(max_length=50, default="0.0.0.0")  # Default IP address
    user_agent = models.TextField(default="Unknown User Agent")  # Default user agent
    location_country = models.CharField(max_length=100, default="Unknown Country")  # Default country
    location_region = models.CharField(max_length=100, default="Unknown Region")  # Default region
    location_city = models.CharField(max_length=100, default="Unknown City")  # Default city
    location_lat = models.FloatField(default=0.0, blank=True, null=True)  # Default latitude
    location_lon = models.FloatField(default=0.0, blank=True, null=True ) # Default longitude
    session_data = models.TextField(default='{"message_history": []}')  # Default session data (JSON format)
    created_at = models.DateTimeField(default=now)  # Session creation time
    expired_at = models.DateTimeField(default=default_expiration_time)

    is_valid = models.BooleanField(default=True)  # Status of the session

    def __str__(self):
        return f"Session {self.session_id} ({self.client_ip})"

   


class Conversation(models.Model):
    session_id = models.CharField(max_length=255, unique=False)  # Session ID to group conversations
    sender = models.CharField(max_length=50, choices=(('user', 'User'), ('bot', 'Bot')))  # Who sent the message
    message = models.TextField()  # Message content
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of the message
    
    def __str__(self):
        return f"{self.session_id} - {self.sender} - {self.timestamp}"
