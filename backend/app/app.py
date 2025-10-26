"""
AI Handwriting OCR API using Flask and EasyOCR

Author: Aritra Chakraborty
Author: Shuvomoy Sarkar
Date: 26-Oct-2025
Description:
-------------
This Flask backend provides an API to extract text from handwritten
or printed images using EasyOCR. It allows clients (e.g., a web
frontend) to upload an image file and receive extracted text in JSON.

Features:
- Single image upload per request
- Only allows image file types specified in .env
- Uses python-dotenv to manage configuration
- CORS enabled for frontend integration
- Temporary file storage with automatic cleanup

Folder Structure:
-----------------
handwriting_ocr_project/
│
├── .venv/                  # Virtual environment
├── .env                    # Environment variables
├── app.py                  # This Flask backend
├── requirements.txt        # Python dependencies
├── uploads/                # Temporary folder for uploaded images
└── ocr_utils/              # OCR helper package
    ├── __init__.py
    ├── reader.py
    ├── preprocess.py
    └── postprocess.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from ocr_utils import extract_text_from_image

# ------------------------------
# Load environment variables from .env
# ------------------------------
load_dotenv()

# ------------------------------
# Flask app initialization
# ------------------------------
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin requests for frontend apps

# ------------------------------
# App configuration from .env
# ------------------------------
# Folder where uploaded images will be temporarily saved
app.config['UPLOAD_FOLDER'] = os.getenv("UPLOAD_FOLDER", "app/uploads")

# Allowed file extensions (e.g., jpg, png)
app.config['ALLOWED_EXTENSIONS'] = set(
    os.getenv("ALLOWED_EXTENSIONS", "jpg,jpeg,png").split(',')
)

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ------------------------------
# Utility functions
# ------------------------------
def allowed_file(filename):
    """
    Check if a file has an allowed extension.
    
    Parameters:
    -----------
    filename : str
        The name of the file to check.

    Returns:
    --------
    bool
        True if the file extension is allowed, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# ------------------------------
# API routes
# ------------------------------
@app.route('/')
def home():
    """
    Root endpoint to verify API is running.

    Returns:
    --------
    JSON
        A simple JSON message indicating the API is active.
    """
    return jsonify({"message": "AI Handwriting OCR API Running..."})

@app.route('/extract-text', methods=['POST'])
def extract_text():
    """
    Endpoint to extract text from an uploaded image.

    Process:
    --------
    1. Verify 'file' is in the request.
    2. Check file name and allowed extension.
    3. Save file temporarily in UPLOAD_FOLDER.
    4. Pass file to OCR utility to extract text.
    5. Remove the temporary file.
    6. Return extracted text as JSON.

    Returns:
    --------
    JSON
        A dictionary containing:
        - 'extracted_text': The text extracted from the uploaded image.
        Or an 'error' message if something went wrong.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file type'}), 400

    # Secure the filename and save temporarily
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Extract text using OCR
    extracted_text = extract_text_from_image(file_path)

    # Remove the uploaded file after processing (optional cleanup)
    os.remove(file_path)

    # Return the extracted text as JSON
    return jsonify({'extracted_text': extracted_text})

# ------------------------------
# Run the Flask app
# ------------------------------
if __name__ == '__main__':
    port = int(os.getenv("PORT", 8000))
    # host='0.0.0.0' makes it accessible from network
    app.run(host='0.0.0.0', port=port, debug=False)
