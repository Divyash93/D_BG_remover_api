from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
import numpy as np
from rembg import remove
import io
import os
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# API Information
API_NAME = "D_BG_remover"
API_VERSION = "1.0.0"
API_DESCRIPTION = "Background removal API powered by rembg"

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_debug_image(image, suffix):
    """Save debug images during processing"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    debug_path = os.path.join(UPLOAD_FOLDER, f'debug_{timestamp}_{suffix}.png')
    image.save(debug_path)
    return debug_path

@app.route('/', methods=['GET'])
def index():
    """API information endpoint"""
    return jsonify({
        'name': API_NAME,
        'version': API_VERSION,
        'description': API_DESCRIPTION,
        'endpoints': {
            'health_check': '/health',
            'remove_background': '/remove-background'
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """API health check endpoint"""
    return jsonify({
        'name': API_NAME,
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/remove-background', methods=['POST'])
def remove_background():
    try:
        # Validate file presence
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        # Validate filename
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({
                'error': 'Invalid file type',
                'allowed_types': list(ALLOWED_EXTENSIONS)
            }), 400
            
        # Validate file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                'error': 'File too large',
                'max_size_mb': MAX_FILE_SIZE / (1024 * 1024)
            }), 400

        # Process the image
        input_image = Image.open(file.stream).convert('RGB')
        
        # Save original for debugging if needed
        if app.debug:
            save_debug_image(input_image, 'input')
        
        # Convert image to NumPy array
        input_array = np.array(input_image)
        
        # Remove background
        output_array = remove(input_array)
        
        # Save processed image for debugging if needed
        if app.debug:
            save_debug_image(Image.fromarray(output_array), 'output')
        
        # Prepare the response
        img_byte_arr = io.BytesIO()
        # Save with high quality
        Image.fromarray(output_array).save(img_byte_arr, format='PNG', quality=95, optimize=True)
        img_byte_arr.seek(0)
        
        # Add branding to output filename
        output_filename = f'D_BG_remover_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'

        return send_file(
            img_byte_arr,
            mimetype='image/png',
            as_attachment=True,
            download_name=output_filename
        )

    except Exception as e:
        app.logger.error(f"{API_NAME} Error: {str(e)}")
        return jsonify({
            'error': 'Failed to process image',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    print(f"Starting {API_NAME} v{API_VERSION}...")
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 