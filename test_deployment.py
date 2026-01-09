"""
Quick deployment test script
Tests if the API is running and accessible
"""

import requests
import time
import sys

API_URL = "http://localhost:8000"

def test_deployment():
    """Test if API is deployed and running."""
    print("=" * 70)
    print("Deployment Test")
    print("=" * 70)
    
    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   [OK] API is running!")
            print(f"   Status: {data.get('status')}")
            print(f"   Model Status: {data.get('model_status')}")
        else:
            print(f"   [FAIL] Unexpected status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   [FAIL] Cannot connect to API")
        print("   Make sure the API server is running:")
        print("   - Run: python api.py")
        print("   - Or double-click: start_api.bat")
        return False
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        return False
    
    # Test 2: Root Endpoint
    print("\n2. Testing Root Endpoint...")
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        if response.status_code == 200:
            print("   [OK] Root endpoint accessible")
        else:
            print(f"   [FAIL] Status: {response.status_code}")
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
    
    # Test 3: Predict Endpoint (with test image)
    print("\n3. Testing Predict Endpoint...")
    import os
    test_image = "yolo/test/images/12_jpg.rf.ee46cb554e7f052492f63ddef74c96a8.jpg"
    
    if os.path.exists(test_image):
        try:
            with open(test_image, 'rb') as f:
                files = {'file': (os.path.basename(test_image), f, 'image/jpeg')}
                data = {'confidence': 0.25}
                response = requests.post(
                    f"{API_URL}/predict",
                    files=files,
                    data=data,
                    timeout=30
                )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   [OK] Prediction successful!")
                print(f"   Detections: {result.get('num_detections', 0)}")
                if result.get('detections'):
                    for i, det in enumerate(result['detections'][:3], 1):
                        print(f"     {i}. {det['class_name']} ({det['confidence']:.2%})")
            else:
                print(f"   [FAIL] Status: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
        except Exception as e:
            print(f"   [FAIL] Error: {e}")
    else:
        print(f"   [SKIP] Test image not found: {test_image}")
    
    # Summary
    print("\n" + "=" * 70)
    print("Deployment Test Complete!")
    print("=" * 70)
    print("\nAPI is deployed and accessible at:")
    print(f"  - Base URL: {API_URL}")
    print(f"  - Health: {API_URL}/health")
    print(f"  - Docs: {API_URL}/docs")
    print(f"  - Predict: {API_URL}/predict")
    print("\nYou can now:")
    print("  - Test with: python test_api.py")
    print("  - Use Postman to send requests")
    print("  - Access API docs in browser")

if __name__ == "__main__":
    test_deployment()
