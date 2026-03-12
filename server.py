import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure upload folder - use system temp dir or local
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize Gemini Client
# It automatically picks up GEMINI_API_KEY from environment variables
try:
    client = genai.Client()
except Exception as e:
    print(f"Warning: Gemini client could not be initialized. Check your API key. Error: {e}")
    client = None

def parse_bookshelf_image(image_path):
    from google.genai import types

    if not client:
        raise Exception("Gemini client not initialized. Please set your GEMINI_API_KEY in the .env file.")

    # We use gemini-2.5-flash which is multimodal and fast
    model = "gemini-2.5-flash"
    
    print(f"Reading {image_path} locally...")
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    
    # Determine mime type naively
    mime_type = "image/jpeg"
    lower_path = image_path.lower()
    if lower_path.endswith(".png"):
        mime_type = "image/png"
    elif lower_path.endswith(".webp"):
        mime_type = "image/webp"
    
    prompt = """
    Analyze this image of a bookshelf. Extract a list of all the visible books.
    Return your response ONLY as a valid JSON array of objects. 
    Each object must have exactly two keys: "title" and "author". 
    If you cannot read an author, put "Unknown".
    Do not wrap the JSON in markdown code blocks. Just valid JSON.
    Example: [{"title": "Dune", "author": "Frank Herbert"}, {"title": "Foundation", "author": "Isaac Asimov"}]
    """
    
    print("Generating content (direct to model)...")
    response = client.models.generate_content(
        model=model,
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            prompt
        ]
    )
        
    try:
        # Sometimes the model still includes markdown formatting
        text = response.text.strip()
        if text.startswith('```json'):
            text = text[7:]
        if text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]
        text = text.strip()
        
        books = json.loads(text)
        return books
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {response.text}")
        raise Exception("Failed to parse the response from the AI.")

@app.route('/api/scan-bookshelf', methods=['POST'])
def scan_bookshelf():
    print("Received request at /api/scan-bookshelf")
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            print(f"File saved to {filepath}. Extracting data...")
            # Call Gemini Vision API
            books = parse_bookshelf_image(filepath)
            
            # Clean up local file
            os.remove(filepath)
            
            return jsonify({"books": books})
        except Exception as e:
            print(f"Error during processing: {e}")
            # Clean up local file on error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    key_exists = bool(os.getenv("GEMINI_API_KEY"))
    return jsonify({"status": "ok", "api_key_configured": key_exists})

if __name__ == '__main__':
    print("Starting server on port 5001...")
    print("Make sure your .env file in the root directory contains GEMINI_API_KEY=your_key_here")
    app.run(debug=True, port=5001)
