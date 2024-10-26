from flask import Flask, render_template, request, jsonify
from PIL import Image
import os
from werkzeug.utils import secure_filename
import base64
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'gallery'
app.config['MAX_CONTENT_LENGTH'] = 2**10 * 2**10

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_img(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except (IOError, SyntaxError):
        return False

def log_status(message):
    with open('logs.txt', 'a') as log_file:
        log_file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] - {message}\n")

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        log_status("Error: No file uploaded")
        return jsonify({"error": "No file"}), 400
    
    file = request.files['file']
    title = request.form.get('title')
    description = request.form.get('description')
    tags = request.form.get('tags')


    if file.filename == '':
        log_status("Error: No selected file")
        return jsonify({"error": "No selected file"}), 400
    

    if file.content_length > 1 * 1024 * 1024: 
        log_status("Error: File size exceeds 1 MB")
        return jsonify({"error": "File size exceeds 1 MB"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        if not is_img(file_path):
            os.remove(file_path)
            log_status("Error: Uploaded file is not a valid image")
            return jsonify({"error": "Uploaded file is not a valid image"}), 400

        file_size = os.path.getsize(file_path) / 1024

        with open(file_path, "rb") as image_file:
            base64_str = base64.b64encode(image_file.read()).decode('utf-8')

        response = {
            "file extension": filename.rsplit('.', 1)[1].lower(),
            "size": round(file_size, 2),
            "description": description,
            "title": title,
            "tags": tags,
            "base64": base64_str
        }

        log_status(f"Success: File {filename} uploaded successfully.")
        return jsonify(response), 200

    else:
        log_status("Error: File type not allowed")
        return jsonify({"error": "File type not allowed"}), 400

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
