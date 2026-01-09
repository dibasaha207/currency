"""
Model Integration & Inference Pipeline
Task 1: Load YOLOv11 model and perform object detection on single images

This script demonstrates:
- Loading trained YOLOv11 model weights
- Performing inference on input images
- Returning detected classes, confidence scores, and bounding box coordinates
"""

import os
import sys
from pathlib import Path
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class TakaNoteDetector:
    """
    Class for performing inference on Bangladeshi Taka notes using YOLOv11 model.
    """
    
    def __init__(self, model_path: str = "models/best.pt"):
        """
        Initialize the detector with trained model weights.
        
        Args:
            model_path: Path to the trained model weights file (.pt)
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model weights not found at {model_path}. "
                "Please ensure the trained model weights are placed in the models/ directory."
            )
        
        print(f"Loading model from {model_path}...")
        self.model = YOLO(model_path)
        print("Model loaded successfully!")
        
        # Class names from data.yaml: ['100 tk', '1000 tk', '200 tk', '500 tk', 'objects']
        self.class_names = ['100 tk', '1000 tk', '200 tk', '500 tk', 'objects']
    
    def predict(self, image_path: str, confidence_threshold: float = 0.25):
        """
        Perform object detection on a single image.
        
        Args:
            image_path: Path to the input image file
            confidence_threshold: Minimum confidence score for detections (default: 0.25)
        
        Returns:
            dict: Dictionary containing detected classes, confidence scores, and bounding boxes
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")
        
        # Perform inference
        results = self.model.predict(
            source=image_path,
            conf=confidence_threshold,
            save=False
        )
        
        # Extract detection results
        detections = []
        result = results[0]
        
        if result.boxes is not None and len(result.boxes) > 0:
            boxes = result.boxes.xyxy.cpu().numpy()  # Bounding boxes in xyxy format
            confidences = result.boxes.conf.cpu().numpy()  # Confidence scores
            class_ids = result.boxes.cls.cpu().numpy().astype(int)  # Class IDs
            
            for i in range(len(boxes)):
                detection = {
                    "class_name": self.class_names[class_ids[i]],
                    "confidence": float(confidences[i]),
                    "bounding_box": {
                        "x1": float(boxes[i][0]),
                        "y1": float(boxes[i][1]),
                        "x2": float(boxes[i][2]),
                        "y2": float(boxes[i][3])
                    }
                }
                detections.append(detection)
        
        return {
            "image_path": image_path,
            "num_detections": len(detections),
            "detections": detections
        }
    
    def visualize(self, image_path: str, output_path: str = None, confidence_threshold: float = 0.25):
        """
        Perform inference and visualize the results.
        
        Args:
            image_path: Path to the input image
            output_path: Path to save the visualized image (optional)
            confidence_threshold: Minimum confidence score for detections
        
        Returns:
            PIL.Image: Visualized image with bounding boxes
        """
        # Perform inference with visualization
        results = self.model.predict(
            source=image_path,
            conf=confidence_threshold,
            save=True if output_path else False
        )
        
        # Load and return the annotated image
        result = results[0]
        if hasattr(result, 'save_dir') and result.save_dir:
            save_dir = result.save_dir
            image_name = Path(image_path).name
            annotated_path = os.path.join(save_dir, image_name)
            if os.path.exists(annotated_path):
                annotated_image = Image.open(annotated_path)
                if output_path:
                    annotated_image.save(output_path)
                return annotated_image
        
        # Fallback: create visualization manually
        img = Image.open(image_path)
        return img


def main():
    """
    Main function to demonstrate inference pipeline.
    """
    print("=" * 70)
    print("Task 1: Model Integration & Inference Pipeline")
    print("=" * 70)
    
    # Initialize detector
    try:
        detector = TakaNoteDetector(model_path="models/best.pt")
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("\nPlease ensure:")
        print("1. The trained model weights (best.pt) are placed in the 'models/' directory")
        print("2. The model was trained in Phase-1 and saved as 'best.pt'")
        sys.exit(1)
    
    # Test with sample images
    test_image_dir = "yolo/test/images"
    if os.path.exists(test_image_dir):
        test_images = [f for f in os.listdir(test_image_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if test_images:
            # Test with first image
            test_image_path = os.path.join(test_image_dir, test_images[0])
            print(f"\nTesting inference on: {test_image_path}")
            print("-" * 70)
            
            # Perform prediction
            results = detector.predict(test_image_path, confidence_threshold=0.25)
            
            # Print results
            print(f"\nImage: {results['image_path']}")
            print(f"Number of detections: {results['num_detections']}")
            
            if results['detections']:
                print("\nDetections:")
                print("-" * 70)
                for i, detection in enumerate(results['detections'], 1):
                    print(f"\n  Detection {i}:")
                    print(f"    Class Name: {detection['class_name']}")
                    print(f"    Confidence Score: {detection['confidence']:.4f}")
                    print(f"    Bounding Box Coordinates:")
                    print(f"      x1: {detection['bounding_box']['x1']:.2f}")
                    print(f"      y1: {detection['bounding_box']['y1']:.2f}")
                    print(f"      x2: {detection['bounding_box']['x2']:.2f}")
                    print(f"      y2: {detection['bounding_box']['y2']:.2f}")
            else:
                print("\nNo detections found in this image.")
            
            # Visualize results
            print("\n" + "-" * 70)
            print("Generating visualization...")
            output_image_path = "inference_output.png"
            annotated_img = detector.visualize(test_image_path, output_path=output_image_path)
            
            # Display the image
            plt.figure(figsize=(12, 8))
            plt.imshow(annotated_img)
            plt.axis('off')
            plt.title("Taka Note Detection Results - Inference Pipeline", fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.savefig(output_image_path, dpi=150, bbox_inches='tight')
            print(f"Visualization saved as '{output_image_path}'")
            print("=" * 70)
            print("Task 1 completed successfully!")
            print("=" * 70)
        else:
            print(f"No test images found in {test_image_dir}")
    else:
        print(f"Test image directory not found: {test_image_dir}")
        print("Please provide a valid image path for testing.")


if __name__ == "__main__":
    main()
