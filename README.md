# Malaria Detection System

A web-based application that uses AI to detect malaria infection from cell images. The system analyzes blood cell images and predicts whether they are infected with malaria parasites or not.

## Features

- **Image Upload**: Drag and drop or click to upload cell images
- **Sample Images**: Test the system with pre-loaded sample images from your dataset
- **Real-time Prediction**: Get instant results with confidence scores
- **Modern UI**: Beautiful, responsive web interface
- **Multiple Formats**: Supports PNG, JPG, JPEG, GIF, and BMP formats

## Prerequisites

- Python 3.7 or higher
- Cell images dataset in the `cell_images/` directory

## Model Download

**Download the trained model (224MB):**
- **Google Drive**: [Download Model](https://drive.google.com/file/d/16imA9-VPF45hMTKflJqSZxotdUSwKJwO/view?usp=drive_link)
- After downloading, rename the file to `my_model.keras copy` and place it in the root directory

## Installation

1. **Clone or download this project** to your local machine

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download and place the model file**:
   - Download the model from the link above
   - Rename it to `my_model.keras copy` and place it in the root directory
   - Your cell images should be in the `cell_images/` directory with subdirectories:
     - `cell_images/Parasitized/` (for infected cells)
     - `cell_images/Uninfected/` (for healthy cells)

## Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Use the application**:
   - **Upload Images**: Click the upload area or drag and drop an image file
   - **Test with Samples**: Click on any sample image to test the prediction
   - **View Results**: See the prediction results with confidence scores

## How it Works

1. **Image Preprocessing**: 
   - Images are resized to 64x64 pixels
   - Converted to RGB format if necessary
   - Normalized to values between 0 and 1

2. **Model Prediction**:
   - The preprocessed image is fed to your trained Keras model
   - The model outputs a probability score
   - Results are classified as "Parasitized" or "Uninfected"

3. **Result Display**:
   - Shows the prediction with confidence level
   - Displays the analyzed image
   - Provides medical disclaimers

## File Structure

```
Malaria_Site/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── my_model.keras copy   # Your trained model
├── templates/
│   └── index.html        # Web interface
├── uploads/              # Temporary upload directory (created automatically)
└── cell_images/          # Your cell images dataset
    ├── Parasitized/      # Infected cell images
    └── Uninfected/       # Healthy cell images
```

## Model Requirements

Your Keras model should:
- Accept input images of size 64x64 pixels
- Output binary classification (infected vs uninfected)
- Be saved in Keras format (`.keras` or `.h5`)

## Troubleshooting

### Common Issues:

1. **Model Loading Error**:
   - Ensure your model file is named correctly
   - Check that the model is compatible with the current TensorFlow version

2. **Image Processing Error**:
   - Verify that uploaded images are in supported formats
   - Check that images are not corrupted

3. **Port Already in Use**:
   - Change the port in `app.py` line: `app.run(debug=True, host='0.0.0.0', port=5001)`

### Performance Tips:

- For better performance, consider using a GPU-enabled TensorFlow installation
- Large model files may take time to load initially
- Processing time depends on image size and model complexity

## Medical Disclaimer

⚠️ **Important**: This application is for educational and research purposes only. It should not be used as a substitute for professional medical diagnosis. Always consult with qualified healthcare professionals for proper medical diagnosis and treatment.

## Technical Details

- **Framework**: Flask (Python web framework)
- **AI Library**: TensorFlow/Keras
- **Image Processing**: Pillow (PIL)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Image Formats**: PNG, JPG, JPEG, GIF, BMP

## Contributing

Feel free to modify and improve this application. Some suggestions:
- Add batch processing capabilities
- Implement user authentication
- Add result history and export features
- Improve the model with additional training data
- Add more detailed analysis reports

## License

This project is open source and available under the MIT License. 