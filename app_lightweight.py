from flask import Flask, render_template, request, jsonify
import os
import numpy as np
from PIL import Image
import base64
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path, target_size=(224, 224)):
    """Preprocess image for model prediction"""
    try:
        img = Image.open(image_path)
        img = img.resize(target_size)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img_array = np.array(img)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def mock_predict_malaria(image_path):
    """Mock prediction for demonstration (replace with actual model)"""
    try:
        # Simulate processing time
        import time
        time.sleep(0.5)
        
        # Generate realistic-looking prediction based on image characteristics
        processed_img = preprocess_image(image_path)
        if processed_img is None:
            return {"error": "Failed to process image"}
        
        # Simple heuristic: check image brightness and contrast
        img_array = processed_img[0]
        brightness = np.mean(img_array)
        contrast = np.std(img_array)
        
        # Simple rule-based prediction (replace with actual model)
        if brightness < 0.4 and contrast > 0.15:
            # Darker images with high contrast might be parasitized
            probability = random.uniform(0.6, 0.9)
            result = "Parasitized (Malaria Positive)"
            confidence = probability
        else:
            # Brighter images might be uninfected
            probability = random.uniform(0.1, 0.4)
            result = "Uninfected (Malaria Negative)"
            confidence = 1 - probability
        
        return {
            "result": result,
            "confidence": round(confidence * 100, 2),
            "probability": round(probability * 100, 2),
            "note": "This is a demonstration prediction. Replace with actual model for production."
        }
        
    except Exception as e:
        return {"error": f"Prediction error: {str(e)}"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Make prediction
        result = mock_predict_malaria(filepath)
        
        # Convert image to base64 for display
        try:
            with open(filepath, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')
                result['image_data'] = f"data:image/png;base64,{img_data}"
        except:
            result['image_data'] = None
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify(result)
    
    return jsonify({'error': 'Invalid file type'})

@app.route('/sample_images')
def get_sample_images():
    """Get sample images from cell_images directory"""
    sample_images = []
    
    parasitized_dir = 'cell_images/Parasitized'
    uninfected_dir = 'cell_images/Uninfected'
    
    try:
        # Get 5 sample parasitized images
        if os.path.exists(parasitized_dir):
            parasitized_files = [f for f in os.listdir(parasitized_dir) if f.endswith('.png')][:5]
            for filename in parasitized_files:
                filepath = os.path.join(parasitized_dir, filename)
                with open(filepath, 'rb') as img_file:
                    img_data = base64.b64encode(img_file.read()).decode('utf-8')
                    sample_images.append({
                        'filename': filename,
                        'data': f"data:image/png;base64,{img_data}",
                        'type': 'Parasitized'
                    })
        
        # Get 5 sample uninfected images
        if os.path.exists(uninfected_dir):
            uninfected_files = [f for f in os.listdir(uninfected_dir) if f.endswith('.png')][:5]
            for filename in uninfected_files:
                filepath = os.path.join(uninfected_dir, filename)
                with open(filepath, 'rb') as img_file:
                    img_data = base64.b64encode(img_file.read()).decode('utf-8')
                    sample_images.append({
                        'filename': filename,
                        'data': f"data:image/png;base64,{img_data}",
                        'type': 'Uninfected'
                    })
    except Exception as e:
        print(f"Error loading sample images: {e}")
    
    return jsonify(sample_images)

@app.route('/predict_sample', methods=['POST'])
def predict_sample():
    """Predict malaria from a sample image"""
    data = request.get_json()
    image_data = data.get('image_data')
    
    if not image_data:
        return jsonify({'error': 'No image data provided'})
    
    try:
        # Decode base64 image
        image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        
        # Save temporarily
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_sample.png')
        with open(temp_path, 'wb') as f:
            f.write(image_bytes)
        
        # Make prediction
        result = mock_predict_malaria(temp_path)
        result['image_data'] = data.get('image_data')
        
        # Clean up
        try:
            os.remove(temp_path)
        except:
            pass
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Error processing sample image: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 