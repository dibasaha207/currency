"""
Setup Verification Script
Verifies that all components are properly set up and ready to run.
"""

import os
import sys
from pathlib import Path


def check_file_exists(filepath, description):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print(f"[OK] {description}: {filepath}")
        return True
    else:
        print(f"[MISSING] {description}: {filepath}")
        return False


def check_directory_exists(dirpath, description):
    """Check if a directory exists."""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        files = os.listdir(dirpath)
        print(f"[OK] {description}: {dirpath} ({len(files)} items)")
        return True
    else:
        print(f"[MISSING] {description}: {dirpath}")
        return False


def main():
    """Main verification function."""
    print("=" * 70)
    print("Project Setup Verification")
    print("=" * 70)
    
    all_ok = True
    
    # Check core files
    print("\n1. Core Files:")
    print("-" * 70)
    all_ok &= check_file_exists("inference.py", "Inference pipeline script")
    all_ok &= check_file_exists("api.py", "REST API script")
    all_ok &= check_file_exists("test_api.py", "API testing script")
    all_ok &= check_file_exists("requirements.txt", "Dependencies file")
    all_ok &= check_file_exists("Dockerfile", "Docker configuration")
    all_ok &= check_file_exists("README.md", "Documentation")
    
    # Check model weights
    print("\n2. Model Weights:")
    print("-" * 70)
    model_exists = check_file_exists("models/best.pt", "Trained model weights")
    if not model_exists:
        print("  [WARNING] Model weights not found. Please copy best.pt to models/")
        all_ok = False
    
    # Check dataset
    print("\n3. Dataset:")
    print("-" * 70)
    check_directory_exists("yolo", "Dataset directory")
    check_file_exists("yolo/data.yaml", "Dataset configuration")
    
    test_images_dir = "yolo/test/images"
    if check_directory_exists(test_images_dir, "Test images directory"):
        test_images = [f for f in os.listdir(test_images_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        print(f"  Found {len(test_images)} test images")
        if len(test_images) >= 5:
            print(f"  [OK] Sufficient test images for Task 3 ({len(test_images)} >= 5)")
        else:
            print(f"  [WARNING] Only {len(test_images)} test images (need at least 5)")
    
    # Check Python packages
    print("\n4. Python Packages:")
    print("-" * 70)
    try:
        import ultralytics
        print("[OK] ultralytics installed")
    except ImportError:
        print("[MISSING] ultralytics - Run: pip install -r requirements.txt")
        all_ok = False
    
    try:
        import fastapi
        print("[OK] fastapi installed")
    except ImportError:
        print("[MISSING] fastapi - Run: pip install -r requirements.txt")
        all_ok = False
    
    try:
        import uvicorn
        print("[OK] uvicorn installed")
    except ImportError:
        print("[MISSING] uvicorn - Run: pip install -r requirements.txt")
        all_ok = False
    
    # Summary
    print("\n" + "=" * 70)
    if all_ok and model_exists:
        print("[SUCCESS] All components are ready!")
        print("\nNext steps:")
        print("  1. Test inference: python inference.py")
        print("  2. Start API: python api.py")
        print("  3. Test API: python test_api.py")
        print("  4. Build Docker: docker build -t taka-note-detector:latest .")
    else:
        print("[ACTION REQUIRED] Some components are missing.")
        if not model_exists:
            print("  - Copy model weights to models/best.pt")
        print("  - Install dependencies: pip install -r requirements.txt")
    print("=" * 70)


if __name__ == "__main__":
    main()
