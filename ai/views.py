from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
import os
from django.contrib.auth import logout
 # Import the KnowledgeBase modelfrom django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .models import Session  # Replace with your actual session model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render
from django.http import JsonResponse
from .utils import create_or_validate_session
import json
from django.shortcuts import render
from .utils import create_or_validate_session
import json

from django.shortcuts import render
import json

import json
import uuid
from django.http import JsonResponse
from django.shortcuts import render
from .models import Session
import logging
from ai.main import process_file

logger = logging.getLogger(__name__)



def delete_sessions(request):
    if request.method == 'POST':
        # Delete all session logs
        Session.objects.all().delete()
        messages.success(request, "All session logs have been cleared.")
        return redirect('log')  # Replace with your actual session logs URL
    return redirect('log')  # In case of a non-POST request, just redirect back


@login_required
def index(request):
    return render(request, 'AI/index.html')   

@login_required
def view_chat_sessions(request):
    return render(request, 'AI/view_sessions.html')

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to dashboard after login
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    
    return render(request, 'AI/login.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('index')  # Replace 'index' with the appropriate view name or URL
        else:
            messages.error(request, 'Please correct the errors above and try again.')   
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'AI/change_password.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def log(request):
     return render(request, 'AI/logs.html')   

def chat(request):
    # Call create_or_validate_session to get the session object
    session = create_or_validate_session(request)

    # Get session_id from the session object
    session_id = session.session_id

    # Prepare the response and pass session data and session_id to the frontend
    response = render(
        request,
        'AI/chat.html',
        {'session_data': json.loads(session.session_data), 'session_id': session_id}
    )

    # Set the session ID in the cookie
    response.set_cookie('session_id', session_id,httponly=True,secure=True,samesite='Lax' )

    return response

def chat_with_doc_route(request):
    try:
        # Get session_id from the cookie or request body
        session_id = request.COOKIES.get('session_id')  # Get session_id from cookies
        data = json.loads(request.body.decode('utf-8'))  # Assuming POST JSON data
        message = data.get('message')
        history = data.get('history', [])
        model_choice = 'OpenAI'
        openai_model_choice = 'gpt-4o-mini'

        # Check if session_id exists in the database
        try:
            session = Session.objects.get(session_id=session_id)
        except Session.DoesNotExist:
            return JsonResponse({
                "history": history + [("You", message), ("Therapist", "Invalid session. Please start a new session.")],
                "error": "Invalid session"
            }, status=400)

        # Process the file (this should be your actual logic)
        conversational_rag_chain = process_file()

        if conversational_rag_chain is None:
            return JsonResponse({
                "history": history + [("You", message), ("Therapist", "Please upload a document first.")]
            })

        # Invoke the conversational RAG chain
        response = conversational_rag_chain.invoke(
            {"input": message},
            config={"configurable": {"session_id": session_id}},
        )

        history.append((message, response['answer']))
        return JsonResponse({"history": history})

    except Exception as e:
        logger.error(f"Error in chat_with_doc_route: {e}", exc_info=True)
        return JsonResponse({
            "history": history + [("You", message), ("Therapist", "An error occurred while processing your request. Please try again later.")],
            "error": str(e)
        }, status=500)

def clear_chat_route(request):
    try:
        session_id = request.COOKIES.get('session_id')  # Get session_id from cookies

        # Check if session_id exists in the database
        try:
            session = Session.objects.get(session_id=session_id)
        except Session.DoesNotExist:
            return JsonResponse({
                "message": "Invalid session. Cannot clear chat.",
            }, status=400)

        # Clear the session data (simulating clearing of store and session)
        session.session_data = {}
        session.save()

        # Generate new session_id
        new_session_id = str(uuid.uuid4())
        session.session_id = new_session_id
        session.save()

        # Return the new session ID and cleared chat history
        response = JsonResponse({"history": [], "message": "Chat cleared."})
        response.set_cookie('session_id', new_session_id, httponly=True, secure=True)  # Set new session_id in the cookie
        return response

    except Exception as e:
        logger.error(f"Error in clear_chat_route: {e}", exc_info=True)
        return JsonResponse({"history": [], "message": "Failed to clear chat. Please try again later."})

def session_logs(request):
    # Fetch all session data
    session_list = SessionData.objects.all()

    # Set up pagination (10 sessions per page)
    paginator = Paginator(session_list, 10)  
    page_number = request.GET.get('page')  # Get the current page number from the request
    sessions = paginator.get_page(page_number)  # Get the sessions for the current page

    return render(request, 'AI/logs.html', {'sessions': sessions})


 
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Session as SessionData
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import shutil
from ai.main import create_db  # Assuming the create_db function is in utils.py or similar.

# Define the upload folder
UPLOAD_FOLDER = os.path.join(settings.BASE_DIR, 'uploads')

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# List of allowed file extensions
ALLOWED_EXTENSIONS = {'csv', 'pdf', 'md', 'txt', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# View to render the main page
def up(request):
    return render(request, 'AI/up.html')

# Handle file upload
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        filename = file.name

        if not allowed_file(filename):
            allowed_file_error = "File type not allowed , try - 'csv', 'pdf', 'md', 'txt', 'docx'"
            return render(request, 'AI/up.html', {'allowed_file_error': allowed_file_error}, status=400)  
        # Save the file
        fs = FileSystemStorage(location=UPLOAD_FOLDER)
        filepath = fs.save(filename, file)

        # Call create_db function
        result = create_db(filepath)

        return render(request, 'AI/up.html',{"result": result})
    

    error =  "No file part in the request" 
    return render(request, 'AI/up.html', {'error': error}, status=400)  


def list_files(request):
    try:
        files = os.listdir(UPLOAD_FOLDER)
        logger.info(f"Files in directory: {files}")  # Log the files found

        if not files:
            message = "No files uploaded yet."
            return render(request, 'AI/up.html', {"files": [], "message": message})  
        
        message = "Files retrieved successfully."
        return render(request, 'AI/up.html', {"files": files, "message": message})
    except Exception as e:
        logger.error(f"Error listing files: {str(e)}")  # Log any error
        return JsonResponse({"error": str(e)}, status=500)  

# Empty the uploads folder
def empty_uploads(request):
    try:
        files = os.listdir(UPLOAD_FOLDER)
        if not files:
            empty_uploads_message = "No files to delete."
            return render(request, 'AI/up.html',{"empty_uploads_message":empty_uploads_message })

        for file in files:
            file_path = os.path.join(UPLOAD_FOLDER, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        empty_uploads_message = "All files deleted successfully."
        return render(request, 'AI/up.html',{"empty_uploads_message":empty_uploads_message })
         
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# Empty the vectorstore folder
def empty_database(request):
    folder_path = os.path.join(settings.BASE_DIR, 'vectorstore')
    try:
        if not os.path.exists(folder_path):

            empty_database_message =  "Folder does not exist. Nothing to delete."
            return render(request, 'AI/up.html',{"empty_database_message":empty_database_message })
        
        shutil.rmtree(folder_path)
        empty_database_message= "Database folder deleted successfully."
        return render(request, 'AI/up.html',{"empty_database_message":empty_database_message })


    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



from django.shortcuts import render
from django.http import JsonResponse
from .models import Conversation
from django.utils.timezone import now

from .models import Conversation
from django.core.exceptions import ValidationError

def save_message(request):
    """Handles saving messages from bot or user."""
    if request.method == "POST":
        # Retrieve and validate the parameters
        session_id = request.POST.get("session_id")
        sender = request.POST.get("sender")  # 'user' or 'bot'
        message = request.POST.get("message")

        # Validate the input data
        if not session_id or not sender or not message:
            return JsonResponse({"status": "error", "message": "All fields are required!"})

        if sender not in ["user", "bot"]:
            return JsonResponse({"status": "error", "message": "Invalid sender type!"})

        try:
            # Save the message
            Conversation.objects.create(
                session_id=session_id,
                sender=sender,
                message=message
            )
            return JsonResponse({"status": "success", "message": "Message saved!"})

        except ValidationError as e:
            return JsonResponse({"status": "error", "message": f"Validation error: {e}"})
        except Exception as e:
            # Catch any other exceptions
            return JsonResponse({"status": "error", "message": f"An error occurred: {e}"})

    return JsonResponse({"status": "error", "message": "Invalid request method!"})


