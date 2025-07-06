#!/usr/bin/env python3
"""
Script to reduce the cell images dataset to 70 images (35 parasitized + 35 uninfected)
by randomly selecting images from the original dataset.
"""

import os
import random
import shutil
from pathlib import Path

def reduce_dataset():
    """Reduce dataset to 70 randomly selected images"""
    
    # Source directories
    parasitized_src = 'cell_images/Parasitized'
    uninfected_src = 'cell_images/Uninfected'
    
    # Create backup of original data
    backup_dir = 'cell_images_backup'
    if not os.path.exists(backup_dir):
        print("Creating backup of original dataset...")
        shutil.copytree('cell_images', backup_dir)
        print(f"✅ Backup created at: {backup_dir}")
    
    # Create new reduced dataset structure
    reduced_dir = 'cell_images_reduced'
    parasitized_dst = os.path.join(reduced_dir, 'Parasitized')
    uninfected_dst = os.path.join(reduced_dir, 'Uninfected')
    
    # Remove existing reduced directory if it exists
    if os.path.exists(reduced_dir):
        shutil.rmtree(reduced_dir)
    
    # Create new directories
    os.makedirs(parasitized_dst, exist_ok=True)
    os.makedirs(uninfected_dst, exist_ok=True)
    
    # Randomly select 35 parasitized images
    if os.path.exists(parasitized_src):
        parasitized_files = [f for f in os.listdir(parasitized_src) if f.endswith('.png')]
        selected_parasitized = random.sample(parasitized_files, min(35, len(parasitized_files)))
        
        print(f"Selecting {len(selected_parasitized)} parasitized images...")
        for filename in selected_parasitized:
            src_path = os.path.join(parasitized_src, filename)
            dst_path = os.path.join(parasitized_dst, filename)
            shutil.copy2(src_path, dst_path)
        print(f"✅ Copied {len(selected_parasitized)} parasitized images")
    
    # Randomly select 35 uninfected images
    if os.path.exists(uninfected_src):
        uninfected_files = [f for f in os.listdir(uninfected_src) if f.endswith('.png')]
        selected_uninfected = random.sample(uninfected_files, min(35, len(uninfected_files)))
        
        print(f"Selecting {len(selected_uninfected)} uninfected images...")
        for filename in selected_uninfected:
            src_path = os.path.join(uninfected_src, filename)
            dst_path = os.path.join(uninfected_dst, filename)
            shutil.copy2(src_path, dst_path)
        print(f"✅ Copied {len(selected_uninfected)} uninfected images")
    
    # Replace original cell_images with reduced dataset
    print("Replacing original dataset with reduced version...")
    shutil.rmtree('cell_images')
    shutil.move(reduced_dir, 'cell_images')
    
    # Print summary
    parasitized_count = len(os.listdir('cell_images/Parasitized'))
    uninfected_count = len(os.listdir('cell_images/Uninfected'))
    total_count = parasitized_count + uninfected_count
    
    print("\n" + "="*50)
    print("DATASET REDUCTION COMPLETE")
    print("="*50)
    print(f"✅ Total images: {total_count}")
    print(f"✅ Parasitized: {parasitized_count}")
    print(f"✅ Uninfected: {uninfected_count}")
    print(f"✅ Original backup saved at: {backup_dir}")
    print("="*50)

if __name__ == "__main__":
    # Set random seed for reproducible results
    random.seed(42)
    
    print("Starting dataset reduction...")
    reduce_dataset()
    print("\nDataset reduction completed successfully!") 