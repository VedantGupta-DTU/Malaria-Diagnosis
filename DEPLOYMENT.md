# Malaria Detection System - Deployment

## Quick Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd Malaria_Site
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the model:**
   - Option A: Download from cloud storage
     ```bash
     python deploy_setup.py --download-model
     ```
   - Option B: Place your model file manually
     - Rename your model to `my_model.keras`
     - Place it in the root directory

4. **Run the application:**
   ```bash
   python app.py
   ```

## Model Download Options

### Option 1: Google Drive
```bash
python deploy_setup.py --gdrive <file-id>
```

### Option 2: Direct URL
```bash
python deploy_setup.py --url <direct-download-url>
```

### Option 3: Manual Download
1. Download the model file from your cloud storage
2. Rename it to `my_model.keras`
3. Place it in the project root directory

## Deployment Platforms

### Heroku
- Add `my_model.keras` to your Heroku app via dashboard
- Or use buildpacks to download during deployment

### Railway/Render
- Use environment variables to specify model download URL
- Or include model in deployment package

### AWS/GCP/Azure
- Store model in cloud storage (S3, GCS, Blob)
- Download during container startup