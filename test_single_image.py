"""
Test inference on a single currency image
You can modify the image_path variable to test different images
"""

from inference import TakaNoteDetector
import os

# Initialize detector
print("Loading model...")
detector = TakaNoteDetector("models/best.pt")

# Specify the image you want to test
# Option 1: Use an image from test folder
image_path = "yolo/test/images/12_jpg.rf.ee46cb554e7f052492f63ddef74c96a8.jpg"  # 1000 tk image

# Option 2: Use your own image (uncomment and set path)
# image_path = "path/to/your/currency/image.jpg"

print(f"\nTesting image: {os.path.basename(image_path)}")
print("="*70)

# Perform detection
results = detector.predict(image_path, confidence_threshold=0.25)

# Display results
print(f"\nNumber of detections: {results['num_detections']}")

if results['detections']:
    print("\nDetected Currency Notes:")
    print("-"*70)
    for i, det in enumerate(results['detections'], 1):
        print(f"\nDetection {i}:")
        print(f"  Denomination: {det['class_name']}")
        print(f"  Confidence: {det['confidence']:.4f} ({det['confidence']*100:.2f}%)")
        print(f"  Bounding Box:")
        print(f"    Top-Left: ({det['bounding_box']['x1']:.1f}, {det['bounding_box']['y1']:.1f})")
        print(f"    Bottom-Right: ({det['bounding_box']['x2']:.1f}, {det['bounding_box']['y2']:.1f})")
        print(f"    Width: {det['bounding_box']['x2'] - det['bounding_box']['x1']:.1f}px")
        print(f"    Height: {det['bounding_box']['y2'] - det['bounding_box']['y1']:.1f}px")
else:
    print("\nNo currency notes detected in this image.")
    print("Try lowering the confidence threshold or using a different image.")

print("\n" + "="*70)
print("Test complete!")
