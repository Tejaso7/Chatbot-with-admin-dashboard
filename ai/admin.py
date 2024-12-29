from django.contrib import admin
from .models import Session

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'created_at', 'is_valid')
    search_fields = ('session_id',)

from .models import Conversation

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'sender', 'timestamp', 'message')
    search_fields = ('session_id', 'message')
    list_filter = ('sender', 'timestamp')