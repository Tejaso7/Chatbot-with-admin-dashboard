from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name='chat'), 
    path('index/', views.index, name='index'),  # Define your views here
    path('view-sessions/', views.view_chat_sessions, name='view_chat_sessions'),
    path('admin/', views.login_view, name='login'),  # Login page
    path('change-password/', views.change_password, name='change_password'),
    path('logout/', views.logout_view, name='logout'), 
    path('log/', views.session_logs, name='log'), 
    path('chat', views.chat_with_doc_route, name='chat_with_doc_route'),
    path('clear_chat', views.clear_chat_route, name='clear_chat_route'),
    path('up/', views.up, name='up'),
    path('upload/', views.upload_file, name='upload_file'),
    path('list_files/', views.list_files, name='list_files'),
    path('empty_uploads/', views.empty_uploads, name='empty_uploads'),
    path('empty_database/', views.empty_database, name='empty_database'),
    path("save_message/", views.save_message, name="save_message"),
    path('delete-sessions/', views.delete_sessions, name='delete_sessions'),
    
]
 
