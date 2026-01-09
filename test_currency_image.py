"""
Quick test script to test inference on currency images
"""

from inference import TakaNoteDetector
import os

# Initialize detector
print("Loading model...")
detector = TakaNoteDetector("models/best.pt")

# Get test images
test_dir = "yolo/test/images"
test_images = [f for f in os.listdir(test_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

print(f"\nFound {len(test_images)} test images")
print("Testing each image...\n")

# Test each image
for idx, img_file in enumerate(test_images[:5], 1):  # Test first 5 images
    img_path = os.path.join(test_dir, img_file)
    print(f"{'='*70}")
    print(f"Image {idx}/{min(5, len(test_images))}: {img_file}")
    print(f"{'='*70}")
    
    try:
        results = detector.predict(img_path, confidence_threshold=0.25)
        
        print(f"Number of detections: {results['num_detections']}")
        
        if results['detections']:
            print("\nDetections:")
            for i, det in enumerate(results['detections'], 1):
                print(f"  {i}. {det['class_name']}")
                print(f"     Confidence: {det['confidence']:.4f}")
                print(f"     Bounding Box: ({det['bounding_box']['x1']:.1f}, {det['bounding_box']['y1']:.1f}) -> "
                      f"({det['bounding_box']['x2']:.1f}, {det['bounding_box']['y2']:.1f})")
        else:
            print("No currency notes detected in this image.")
        
        print()
        
    except Exception as e:
        print(f"Error processing image: {e}\n")

print("="*70)
print("Testing complete!")
print("="*70)
