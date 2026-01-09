"""
REST API Development - Task 2
FastAPI implementation for serving the YOLOv11 model via REST API.

API Endpoint: /predict
HTTP Method: POST
Input: Image file (JPEG/PNG)
Output: JSON with detected denomination names, confidence scores, and bounding box coordinates
"""

import os
import io
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ultralytics import YOLO
from PIL import Image
import uvicorn
import numpy as np


# Initialize FastAPI app
app = FastAPI(
    title="Bangladeshi Taka Note Detection API",
    description="REST API for detecting Bangladeshi Taka notes using YOLOv11",
    version="1.0.0"
)

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model variable
model = None
class_names = ['100 tk', '1000 tk', '200 tk', '500 tk', 'objects']


# Response models
class BoundingBox(BaseModel):
    """Bounding box coordinates in xyxy format."""
    x1: float
    y1: float
    x2: float
    y2: float


class Detection(BaseModel):
    """Single detection result."""
    class_name: str
    confidence: float
    bounding_box: BoundingBox


class PredictionResponse(BaseModel):
    """API response model."""
    success: bool
    num_detections: int
    detections: List[Detection]
    message: Optional[str] = None


def load_model(model_path: str = "models/best.pt"):
    """
    Load the trained YOLOv11 model.
    
    Args:
        model_path: Path to the model weights file
    """
    global model
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model weights not found at {model_path}. "
            "Please ensure the trained model weights are placed in the models/ directory."
        )
    
    print(f"Loading model from {model_path}...")
    model = YOLO(model_path)
    print("Model loaded successfully!")


@app.on_event("startup")
async def startup_event():
    """Load model when the API starts."""
    try:
        load_model()
    except FileNotFoundError as e:
        print(f"Warning: {e}")
        print("API will start but /predict endpoint will return errors until model is available.")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Bangladeshi Taka Note Detection API",
        "version": "1.0.0",
        "task": "Task 2: REST API Development",
        "endpoints": {
            "/predict": "POST - Upload an image for detection",
            "/health": "GET - Check API health status",
            "/docs": "GET - API documentation (Swagger UI)"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    model_status = "loaded" if model is not None else "not loaded"
    return {
        "status": "healthy",
        "model_status": model_status
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...), confidence: float = 0.25):
    """
    Predict endpoint for object detection on uploaded images.
    
    Args:
        file: Image file (JPEG/PNG)
        confidence: Confidence threshold (default: 0.25)
    
    Returns:
        JSON response with detections including:
        - Detected denomination names
        - Confidence scores
        - Bounding box coordinates
    """
    # Validate model is loaded
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded. Please ensure model weights are available."
        )
    
    # Handle invalid or missing inputs gracefully
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload an image file (JPEG/PNG)"
        )
    
    # Validate confidence threshold
    if not 0.0 <= confidence <= 1.0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Confidence threshold must be between 0.0 and 1.0"
        )
    
    try:
        # Read image file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert PIL Image to numpy array for YOLO
        image_array = np.array(image)
        
        # Perform inference
        results = model.predict(
            source=image_array,
            conf=confidence,
            save=False,
            verbose=False
        )
        
        # Extract detection results
        detections = []
        result = results[0]
        
        if result.boxes is not None and len(result.boxes) > 0:
            boxes = result.boxes.xyxy.cpu().numpy()  # Bounding boxes
            confidences = result.boxes.conf.cpu().numpy()  # Confidence scores
            class_ids = result.boxes.cls.cpu().numpy().astype(int)  # Class IDs
            
            for i in range(len(boxes)):
                detection = Detection(
                    class_name=class_names[class_ids[i]],
                    confidence=float(confidences[i]),
                    bounding_box=BoundingBox(
                        x1=float(boxes[i][0]),
                        y1=float(boxes[i][1]),
                        x2=float(boxes[i][2]),
                        y2=float(boxes[i][3])
                    )
                )
                detections.append(detection)
        
        # Return appropriate HTTP status code and JSON response
        return PredictionResponse(
            success=True,
            num_detections=len(detections),
            detections=detections,
            message="Detection completed successfully"
        )
    
    except Exception as e:
        # Handle errors gracefully with appropriate status code
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing image: {str(e)}"
        )


if __name__ == "__main__":
    # Run the API server
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
