from flask import Flask, request, send_file
from spleeter.separator import Separator
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
separator = Separator('spleeter:2stems')

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/process', methods=['POST'])
def process_audio():
    if 'file' not in request.files:
        return {"error": "No file provided"}, 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(PROCESSED_FOLDER, filename)

    file.save(input_path)

    separator.separate_to_file(input_path, PROCESSED_FOLDER)

    instrumental_path = os.path.join(PROCESSED_FOLDER, filename.replace('.mp3', ''), 'accompaniment.wav')

    if not os.path.exists(instrumental_path):
        return {"error": "Failed to process file"}, 500

    return send_file(instrumental_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)