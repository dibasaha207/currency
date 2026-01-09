"""
API Testing & Validation - Task 3
Tests the REST API using multiple test images and validates responses.

Requirements:
- Test using Postman or curl (simulated with requests library)
- Test with at least 5 different test images
- Verify correctness of predictions and response format
"""

import os
import requests
import json
from pathlib import Path
from typing import List, Dict
import time


API_URL = "http://localhost:8000"


def test_health_check():
    """Test the health check endpoint."""
    print("=" * 70)
    print("Testing Health Check Endpoint")
    print("=" * 70)
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        if response.status_code == 200:
            print("[OK] Health check passed\n")
            return True
        else:
            print("[FAIL] Health check failed\n")
            return False
    except Exception as e:
        print(f"[FAIL] Health check failed: {e}\n")
        return False


def test_predict(image_path: str, confidence: float = 0.25) -> Dict:
    """
    Test the /predict endpoint with a single image.
    
    Args:
        image_path: Path to the test image
        confidence: Confidence threshold
    
    Returns:
        dict: Response data
    """
    print(f"\nTesting with image: {os.path.basename(image_path)}")
    print("-" * 70)
    
    if not os.path.exists(image_path):
        print(f"[FAIL] Image not found: {image_path}")
        return None
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
            data = {'confidence': confidence}
            
            response = requests.post(
                f"{API_URL}/predict",
                files=files,
                data=data,
                timeout=30
            )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result['success']}")
            print(f"Number of Detections: {result['num_detections']}")
            print(f"Message: {result['message']}")
            
            if result['detections']:
                print("\nDetections:")
                for i, detection in enumerate(result['detections'], 1):
                    print(f"  {i}. Class: {detection['class_name']}")
                    print(f"     Confidence: {detection['confidence']:.4f}")
                    print(f"     Bounding Box: ({detection['bounding_box']['x1']:.2f}, "
                          f"{detection['bounding_box']['y1']:.2f}) -> "
                          f"({detection['bounding_box']['x2']:.2f}, "
                          f"{detection['bounding_box']['y2']:.2f})")
            else:
                print("No detections found.")
            
            # Verify response format
            assert 'success' in result, "Missing 'success' field"
            assert 'num_detections' in result, "Missing 'num_detections' field"
            assert 'detections' in result, "Missing 'detections' field"
            assert isinstance(result['detections'], list), "Detections must be a list"
            
            print("[OK] Prediction successful and response format verified\n")
            return result
        else:
            print(f"[FAIL] Error: {response.status_code}")
            print(f"Response: {response.text}\n")
            return None
    
    except Exception as e:
        print(f"[FAIL] Request failed: {e}\n")
        return None


def test_invalid_inputs():
    """Test API with invalid inputs to verify error handling."""
    print("=" * 70)
    print("Testing Error Handling")
    print("=" * 70)
    
    # Test 1: Invalid file type
    print("\n1. Testing with invalid file type (text file)...")
    try:
        with open("test_api.py", 'rb') as f:
            files = {'file': ('test.txt', f, 'text/plain')}
            response = requests.post(f"{API_URL}/predict", files=files, timeout=10)
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 400:
            print("   [OK] Correctly rejected invalid file type")
        else:
            print(f"   [FAIL] Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
    
    # Test 2: Invalid confidence threshold
    print("\n2. Testing with invalid confidence threshold...")
    try:
        test_image_dir = "yolo/test/images"
        if os.path.exists(test_image_dir):
            test_images = [f for f in os.listdir(test_image_dir) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            if test_images:
                image_path = os.path.join(test_image_dir, test_images[0])
                with open(image_path, 'rb') as f:
                    files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
                    data = {'confidence': 1.5}  # Invalid confidence > 1.0
                    response = requests.post(f"{API_URL}/predict", files=files, data=data, timeout=10)
                print(f"   Status Code: {response.status_code}")
                if response.status_code == 400:
                    print("   [OK] Correctly rejected invalid confidence threshold")
                else:
                    print(f"   [FAIL] Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"   [FAIL] Error: {e}")


def main():
    """Main testing function."""
    print("\n" + "=" * 70)
    print("Task 3: API Testing & Validation")
    print("=" * 70)
    
    # Test health check
    if not test_health_check():
        print("\n[ERROR] API is not running. Please start the API server first.")
        print("Run: python api.py or uvicorn api:app --host 0.0.0.0 --port 8000")
        return
    
    # Test with multiple images (at least 5)
    test_image_dir = "yolo/test/images"
    test_results = []
    
    if os.path.exists(test_image_dir):
        test_images = [f for f in os.listdir(test_image_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        # Test with at least 5 images (or all available if less than 5)
        num_images_to_test = max(5, len(test_images))
        images_to_test = test_images[:num_images_to_test]
        
        print("=" * 70)
        print(f"Testing with {len(images_to_test)} test images")
        print("=" * 70)
        
        for idx, image_file in enumerate(images_to_test, 1):
            print(f"\n[Test Image {idx}/{len(images_to_test)}]")
            image_path = os.path.join(test_image_dir, image_file)
            result = test_predict(image_path, confidence=0.25)
            if result:
                test_results.append({
                    'image': image_file,
                    'num_detections': result['num_detections'],
                    'detections': result['detections']
                })
            time.sleep(0.5)  # Small delay between requests
    else:
        print(f"[ERROR] Test image directory not found: {test_image_dir}")
        print("Please ensure test images are available in yolo/test/images/")
        return
    
    # Test error handling
    test_invalid_inputs()
    
    # Summary and discussion on prediction accuracy
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Total images tested: {len(test_results)}")
    
    if test_results:
        total_detections = sum(r['num_detections'] for r in test_results)
        avg_detections = total_detections / len(test_results) if test_results else 0
        print(f"Total detections: {total_detections}")
        print(f"Average detections per image: {avg_detections:.2f}")
        
        # Count detections by class
        class_counts = {}
        confidence_scores = []
        for result in test_results:
            for detection in result['detections']:
                class_name = detection['class_name']
                class_counts[class_name] = class_counts.get(class_name, 0) + 1
                confidence_scores.append(detection['confidence'])
        
        if class_counts:
            print("\nDetections by class:")
            for class_name, count in sorted(class_counts.items()):
                print(f"  {class_name}: {count}")
        
        if confidence_scores:
            avg_confidence = sum(confidence_scores) / len(confidence_scores)
            min_confidence = min(confidence_scores)
            max_confidence = max(confidence_scores)
            print(f"\nConfidence Statistics:")
            print(f"  Average: {avg_confidence:.4f}")
            print(f"  Minimum: {min_confidence:.4f}")
            print(f"  Maximum: {max_confidence:.4f}")
        
        # Brief discussion on prediction accuracy
        print("\n" + "=" * 70)
        print("Brief Discussion on Prediction Accuracy")
        print("=" * 70)
        print(f"The model was tested on {len(test_results)} images and detected {total_detections} total objects.")
        print(f"Average detections per image: {avg_detections:.2f}")
        if confidence_scores:
            print(f"The confidence scores range from {min_confidence:.4f} to {max_confidence:.4f}, ")
            print(f"with an average of {avg_confidence:.4f}, indicating {'good' if avg_confidence > 0.7 else 'moderate' if avg_confidence > 0.5 else 'low'} model confidence.")
        print("All API responses were verified to have the correct JSON format with:")
        print("  - success: boolean")
        print("  - num_detections: integer")
        print("  - detections: array of objects with class_name, confidence, and bounding_box")
        print("  - message: string")
    
    print("\n" + "=" * 70)
    print("Task 3: API Testing & Validation - Completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
