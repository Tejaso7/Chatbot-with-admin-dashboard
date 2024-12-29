from flask import Flask, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
from main import *
import logging
#from main_vectorstore import create_db

app = Flask(__name__)

# Configurations
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'pdf', 'md', 'txt', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('user.html')

@app.route('/client')
def index1():
    return render_template('client.html')

@app.route('/test')
def test():
    return jsonify({"message": "Test route working!"})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Call the create_db function from main.py
        result = create_db(filepath)
        return jsonify({"message": result})
    else:
        return jsonify({"error": "File type not allowed"}), 400

@app.route('/list_files', methods=['POST'])
def list_files():
    try:
        # Ensure the upload folder exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            return jsonify({"files": [], "message": "No files uploaded yet."})
        
        # List all files in the upload folder
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        if not files:
            return jsonify({"files": [], "message": "No files uploaded yet."})
        
        # Return the list of files
        return jsonify({"files": files, "message": "Files retrieved successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/empty_uploads', methods=['POST'])
def empty_uploads():
    try:
        # Ensure the upload folder exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            return jsonify({"message": "Upload folder does not exist. No files to delete."})
        
        # List all files in the folder
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        
        if not files:
            return jsonify({"message": "No files to delete."})
        
        # Delete all files in the folder
        for file in files:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        return jsonify({"message": "All files deleted successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/empty_database', methods=['POST'])
def empty_database():
    folder_path = 'vectorstore'
    
    try:
        # Check if the folder exists
        if not os.path.exists(folder_path):
            return jsonify({"message": "Folder does not exist. Nothing to delete."})
        
        # Remove the folder and all its contents
        shutil.rmtree(folder_path)
        return jsonify({"message": "Database folder deleted successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat_with_doc_route():
    try:
        data = request.json
        message = data.get('message')
        history = data.get('history', [])
        model_choice = 'OpenAI'
        openai_model_choice = 'gpt-4o-mini'
        conversational_rag_chain=process_file()


        if conversational_rag_chain is None:
            return jsonify(history=history + [("You", message), ("Guru JI", "Please upload a document first.")])

        response = conversational_rag_chain.invoke(
            {"input": message},
            config={"configurable": {"session_id": session_id}},
        )

        history.append((message, response['answer']))
        #print(history)
        #response['answer'] #
        return jsonify(history=history)
    except Exception as e:
        logger.error(f"Error in chat_with_doc_route: {e}", exc_info=True)
        return jsonify(history=history + [("You", message), ("Guru JI", "An error occurred while processing your request. Please try again later.")])

@app.route('/clear_chat', methods=['POST'])
def clear_chat_route():
    try:
        global store, session_id
        store.clear()
        session_id = str(uuid.uuid4())
        return jsonify(history=[], message="Chat cleared.")
    except Exception as e:
        logger.error(f"Error in clear_chat_route: {e}", exc_info=True)
        return jsonify(history=[], message="Failed to clear chat. Please try again later.")



if __name__ == '__main__':
    app.run(debug=True)
