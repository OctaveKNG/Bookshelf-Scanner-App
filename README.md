# Bookshelf Scanner App (Lumina)
<div align="center">
  <img src="assets/Capture d'écran 2026-03-12 171535.png" alt="Lumina Bookshelf Scanner App Screenshot" width="600"/>
</div>

<div align="center">
  <img src="assets/Capture d'écran 2026-03-12 171454.png" alt="Lumina Bookshelf Scanner App Screenshot" width="600"/>
</div>




Turn your bookshelf photos into a customized digital library instantly using AI! 

Lumina is a lightweight, responsive web application that allows users to upload a photo of their bookshelf. It uses the **Google Gemini Vision API** to analyze the image, extract the visible books (titles and authors), and returns a clean digital list.

## 🚀 Features
- **Premium UI:** Glassmorphism design, dark mode, smooth micro-animations.
- **Drag & Drop Upload:** Easy photo upload or file selection.
- **Real-time AI Processing:** Utilizes `gemini-2.5-flash` for rapid multimodal image analysis.
- **No Database Config:** Simple standalone architecture.

## 🛠 Tech Stack
- **Frontend:** Vanilla HTML, CSS (Custom Properties, Flexbox), JavaScript
- **Backend:** Python, Flask, Flask-CORS
- **AI Integration:** Google GenAI SDK (`google-genai`)

## 📋 Prerequisites
- Python 3.8+
- A free [Google Gemini API Key](https://aistudio.google.com/)

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd bookshelf-app
   ```

2. **Set up the Python Virtual Environment:**
   *(Windows)*
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
   *(Mac/Linux)*
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install Flask flask-cors google-genai python-dotenv werkzeug pillow
   ```
   *(Alternatively, if a `requirements.txt` is provided in the future, run `pip install -r requirements.txt`)*

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## ▶️ Running the Application

Because this app uses separate front and back ends in the same folder during development, you need two terminal windows:

**Terminal 1 (Backend Server):**
```bash
# Make sure your virtual environment is activated!
python server.py
# Server should start on http://localhost:5001
```

**Terminal 2 (Frontend Client):**
```bash
# Start a simple HTTP server for the frontend files
python -m http.server 8080
# Open your browser to http://localhost:8080
```

## 📸 Usage
1. Open the UI at `http://localhost:8080`
2. Drag and drop an image of a bookshelf (JPG, PNG, WEBP).
3. Wait for the AI to process the image (usually 5-15 seconds).
4. View your extracted digital library! 

## 💡 Similar Projects & Inspiration
If you're interested in alternative approaches or expanding this project, check out these excellent repositories that tackle similar challenges:

- [suxrobGM/bookshelf-scanner](https://github.com/suxrobGM/bookshelf-scanner) - Uses OCR, YOLO segmentation, and local LLMs (Moondream2) to extract titles and authors.
- [jukasdrj/books-tracker-v1](https://github.com/jukasdrj/books-tracker-v1) - Features an AI-powered Bookshelf Scanner powered by Gemini 2.0 Flash to identify books from photos and track reading progress.
- [Jybbs/Bookshelf-Scanner](https://github.com/Jybbs/Bookshelf-Scanner) - An experimental repository focused on extracting bookshelf data.

## 📝 License
MIT License
