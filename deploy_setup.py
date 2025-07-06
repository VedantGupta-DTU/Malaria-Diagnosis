#!/usr/bin/env python3
"""
Deployment setup script for Malaria Detection System
This script helps set up the application for deployment without including the large model file.
"""

import os
import requests
import zipfile
from pathlib import Path

def download_model_from_url(url, filename="my_model.keras"):
    """Download model from a cloud storage URL"""
    print(f"Downloading model from {url}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Model downloaded successfully: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        return False

def create_deployment_files():
    """Create deployment-specific files"""
    
    # Create .gitignore for deployment
    gitignore_content = """
# Model files (too large for git)
my_model.keras*
*.h5
*.pb

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Flask
instance/
.webassets-cache

# Uploads
uploads/
*.png
*.jpg
*.jpeg

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content.strip())
    
    # Create deployment README
    deploy_readme = """
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
"""
    
    with open('DEPLOYMENT.md', 'w') as f:
        f.write(deploy_readme.strip())
    
    print("✅ Created deployment files")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Malaria Detection System Deployment Setup')
    parser.add_argument('--download-model', action='store_true', help='Download model from default URL')
    parser.add_argument('--url', type=str, help='Download model from specific URL')
    parser.add_argument('--gdrive', type=str, help='Download model from Google Drive file ID')
    parser.add_argument('--setup', action='store_true', help='Create deployment files')
    
    args = parser.parse_args()
    
    if args.setup:
        create_deployment_files()
    
    if args.url:
        download_model_from_url(args.url)
    elif args.gdrive:
        gdrive_url = f"https://drive.google.com/uc?id={args.gdrive}"
        download_model_from_url(gdrive_url)
    elif args.download_model:
        # Default to the provided Google Drive link
        gdrive_id = "16imA9-VPF45hMTKflJqSZxotdUSwKJwO"
        gdrive_url = f"https://drive.google.com/uc?id={gdrive_id}"
        print(f"Downloading model from Google Drive (ID: {gdrive_id})...")
        download_model_from_url(gdrive_url)

if __name__ == "__main__":
    main() 