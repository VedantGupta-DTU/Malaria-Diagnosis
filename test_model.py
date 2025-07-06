#!/usr/bin/env python3
"""
Test script to verify model loading and basic functionality
"""

import tensorflow as tf
import numpy as np
from PIL import Image
import os

def test_model_loading():
    """Test if the model can be loaded successfully"""
    print("Testing model loading...")
    
    model = None
    
    # Try different loading approaches
    try:
        # First try: direct load
        model = tf.keras.models.load_model('my_model.keras copy')
        print("✅ Model loaded successfully using direct load!")
        
        # Print model summary
        print("\nModel Summary:")
        model.summary()
        
        # Test with a dummy image
        print("\nTesting with dummy image...")
        dummy_image = np.random.rand(1, 224, 224, 3)
        prediction = model.predict(dummy_image)
        print(f"✅ Prediction shape: {prediction.shape}")
        print(f"✅ Prediction value: {prediction[0]}")
        
        return True
        
    except Exception as e:
        print(f"Direct load failed: {e}")
        
        try:
            # Second try: using TFSMLayer
            from tensorflow import keras
            model = keras.layers.TFSMLayer('my_model.keras copy', call_endpoint='serving_default')
            print("✅ Model loaded successfully using TFSMLayer!")
            
            # Test with a dummy image
            print("\nTesting with dummy image...")
            dummy_image = np.random.rand(1, 224, 224, 3)
            prediction = model(dummy_image)
            if isinstance(prediction, dict):
                prediction = list(prediction.values())[0]
            print(f"✅ Prediction shape: {prediction.shape}")
            print(f"✅ Prediction value: {prediction[0]}")
            
            return True
            
        except Exception as e2:
            print(f"TFSMLayer load failed: {e2}")
            
            try:
                # Third try: rename and load
                import shutil
                shutil.copy('my_model.keras copy', 'my_model.keras')
                model = tf.keras.models.load_model('my_model.keras')
                print("✅ Model loaded successfully after renaming!")
                
                # Test with a dummy image
                print("\nTesting with dummy image...")
                dummy_image = np.random.rand(1, 224, 224, 3)
                prediction = model.predict(dummy_image)
                print(f"✅ Prediction shape: {prediction.shape}")
                print(f"✅ Prediction value: {prediction[0]}")
                
                return True
                
            except Exception as e3:
                print(f"Renamed file load failed: {e3}")
                return False

def test_image_processing():
    """Test image processing functionality"""
    print("\nTesting image processing...")
    
    # Check if sample images exist
    parasitized_dir = 'cell_images/Parasitized'
    uninfected_dir = 'cell_images/Uninfected'
    
    if os.path.exists(parasitized_dir):
        parasitized_files = [f for f in os.listdir(parasitized_dir) if f.endswith('.png')]
        print(f"✅ Found {len(parasitized_files)} parasitized images")
    else:
        print("❌ Parasitized directory not found")
    
    if os.path.exists(uninfected_dir):
        uninfected_files = [f for f in os.listdir(uninfected_dir) if f.endswith('.png')]
        print(f"✅ Found {len(uninfected_files)} uninfected images")
    else:
        print("❌ Uninfected directory not found")
    
    # Test processing a sample image if available
    if os.path.exists(parasitized_dir) and parasitized_files:
        sample_file = os.path.join(parasitized_dir, parasitized_files[0])
        try:
            img = Image.open(sample_file)
            img = img.resize((224, 224))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            print(f"✅ Sample image processed successfully. Shape: {img_array.shape}")
        except Exception as e:
            print(f"❌ Error processing sample image: {e}")

def main():
    """Main test function"""
    print("=" * 50)
    print("MALARIA DETECTION SYSTEM - MODEL TEST")
    print("=" * 50)
    
    # Test model loading
    model_ok = test_model_loading()
    
    # Test image processing
    test_image_processing()
    
    print("\n" + "=" * 50)
    if model_ok:
        print("✅ All tests passed! You can run the web application.")
        print("Run: python app.py")
    else:
        print("❌ Model loading failed. Please check your model file.")
    print("=" * 50)

if __name__ == "__main__":
    main() 