from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import numpy as np
from PIL import Image
import tensorflow as tf
from werkzeug.utils import secure_filename
import base64
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the model
try:
    # Try different model loading approaches
    model = None
    
    # First try: direct load
    try:
        model = tf.keras.models.load_model('my_model.keras copy')
        print("Model loaded successfully!")
    except:
        # Second try: using TFSMLayer for SavedModel format
        try:
            from tensorflow import keras
            model = keras.layers.TFSMLayer('my_model.keras copy', call_endpoint='serving_default')
            print("Model loaded using TFSMLayer!")
        except:
            # Third try: rename file and try again
            try:
                import shutil
                shutil.copy('my_model.keras copy', 'my_model.keras')
                model = tf.keras.models.load_model('my_model.keras')
                print("Model loaded after renaming!")
            except Exception as e:
                print(f"Error loading model: {e}")
                model = None
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path, target_size=(224, 224)):
    """Preprocess image for model prediction"""
    try:
        # Load and resize image
        img = Image.open(image_path)
        img = img.resize(target_size)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Convert to array and normalize
        img_array = np.array(img)
        img_array = img_array / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def predict_malaria(image_path):
    """Predict malaria from image"""
    if model is None:
        return {"error": "Model not loaded"}
    
    try:
        # Preprocess image
        processed_img = preprocess_image(image_path)
        if processed_img is None:
            return {"error": "Failed to process image"}
        
        # Make prediction
        if hasattr(model, 'predict'):
            # Standard Keras model
            prediction = model.predict(processed_img)
        else:
            # TFSMLayer model
            prediction = model(processed_img)
            if isinstance(prediction, dict):
                # Extract the first value from the dictionary
                prediction = list(prediction.values())[0]
        
        # Handle different prediction formats
        if len(prediction.shape) == 1:
            # Single value output
            probability = float(prediction[0])
        elif prediction.shape[1] == 1:
            # Single column output
            probability = float(prediction[0][0])
        else:
            # Multiple columns, assume second column is positive class
            probability = float(prediction[0][1])
        
        # Determine result (reversed logic)
        if probability > 0.5:
            result = "Uninfected (Malaria Negative)"
            confidence = probability
        else:
            result = "Parasitized (Malaria Positive)"
            confidence = 1 - probability
        
        return {
            "result": result,
            "confidence": round(confidence * 100, 2),
            "probability": round(probability * 100, 2)
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
        result = predict_malaria(filepath)
        
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
    
    # Get some sample images from both directories
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
        image_data = image_data.split(',')[1]  # Remove data URL prefix
        image_bytes = base64.b64decode(image_data)
        
        # Save temporarily
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_sample.png')
        with open(temp_path, 'wb') as f:
            f.write(image_bytes)
        
        # Make prediction
        result = predict_malaria(temp_path)
        result['image_data'] = data.get('image_data')  # Return original image data
        
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