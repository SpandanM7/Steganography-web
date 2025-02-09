from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from steganography import embed_data, retrieve_data

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/embed', methods=['POST'])
def embed():
    # Get the image and text from the request
    image = request.files['image']
    text = request.form['text']
    
    # Save the uploaded image
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)
    
    # Embed the text into the image
    output_image_path = os.path.join(UPLOAD_FOLDER, 'stego_' + image.filename)
    embed_data(image_path, text, output_image_path)
    
    # Return the stego image
    return send_file(output_image_path, mimetype='image/png')

@app.route('/retrieve', methods=['POST'])
def retrieve():
    # Get the stego image from the request
    stego_image = request.files['stego_image']
    
    # Save the uploaded stego image
    stego_image_path = os.path.join(UPLOAD_FOLDER, stego_image.filename)
    stego_image.save(stego_image_path)
    
    # Retrieve the text from the stego image
    extracted_text = retrieve_data(stego_image_path)
    
    # Return the extracted text
    return jsonify({'text': extracted_text})

if __name__ == '__main__':
    app.run(debug=True)