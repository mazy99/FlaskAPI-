from flask import Flask, render_template, request, jsonify
from PIL import Image
import os
import base64
from io import BytesIO
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'gallery'
app.config['MAX_CONTENT_LENGTH'] = 1024*1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(extension):
    return extension in ALLOWED_EXTENSIONS

def log_status(message):
    with open('logs.txt', 'a') as log_file:
        log_file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] - {message}\n")

@app.route('/')
def upload_form():
    return render_template('index2.html')

@app.route('/image', methods=['POST'])
def upload_file():
    data = request.get_json()  
    if not data:
        log_status("Error: No data received")
        return jsonify({"error": "No data received"}), 400


    img_base64 = data.get('base64')
    title = data.get('title')
    description = data.get('description')
    tags = data.get('tags')
    extension = data.get('extension')
    file_size = data.get('size')

    if not img_base64 or not allowed_file(extension):
        log_status("Error: Invalid image data or unsupported file extension")
        return jsonify({"error": "Invalid image data or unsupported file extension"}), 400

    try:
        
        img_data = base64.b64decode(img_base64.split(",")[1])  
        img = Image.open(BytesIO(img_data))

        filename = f"{title or 'uploaded_image'}.{extension}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        img.save(file_path)

        
        log_status(f"Success: File {filename} uploaded successfully.")
        response = {
            "file extension": extension,
            "size": file_size,
            "description": description,
            "title": title,
            "tags": tags,
            "message": "Файл успешно загружен!"
        }
        return jsonify(response), 200

    except Exception as e:
        log_status(f"Error during file processing: {str(e)}")
        return jsonify({"error": "Error processing file"}), 500

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
