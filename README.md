<<<<<<< HEAD
# Deployment of Bangladeshi Taka Note Detection Model Using REST API & Docker

## Project Overview

This project implements a complete deployment solution for a YOLOv11-based Bangladeshi Taka note detection model. The system includes an inference pipeline, REST API, comprehensive testing, Docker containerization, and full documentation.

**Model Classes:** 100 tk, 200 tk, 500 tk, 1000 tk, objects

---

## 📋 Table of Contents

- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Task 1: Model Integration & Inference Pipeline](#task-1-model-integration--inference-pipeline)
- [Task 2: REST API Development](#task-2-rest-api-development)
- [Task 3: API Testing & Validation](#task-3-api-testing--validation)
- [Task 4: Dockerization](#task-4-dockerization)
- [Task 5: Deployment & Documentation](#task-5-deployment--documentation)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)

---

## 📁 Project Structure

```
module 12/
│
├── inference.py          # Task 1: Inference pipeline
├── api.py                # Task 2: FastAPI REST API
├── test_api.py           # Task 3: API testing script
├── requirements.txt      # Python dependencies
├── Dockerfile           # Task 4: Docker configuration
├── README.md            # This file (Task 5)
│
├── models/              # Model weights directory
│   └── best.pt         # Trained YOLOv11 model (from Phase-1)
│
└── yolo/               # Dataset directory
    ├── data.yaml       # Dataset configuration
    ├── train/          # Training images and labels
    ├── valid/          # Validation images and labels
    └── test/           # Test images and labels
```

---

## 🔧 Prerequisites

- **Python 3.11+**
- **Docker** (for Task 4)
- **Trained model weights** (`best.pt`) from Phase-1
- **Git** (optional)

---

## 📦 Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Model Weights

Place your trained model weights from Phase-1 in the `models/` directory:

```bash
# Create models directory
mkdir models

# Copy your trained model
# Windows:
copy "runs\detect\currency detection\weights\best.pt" models\best.pt

# Linux/Mac:
cp "runs/detect/currency detection/weights/best.pt" models/best.pt
```

**Verify:**
```bash
# Windows
dir models\best.pt

# Linux/Mac
ls models/best.pt
```

---

## 🎯 Task 1: Model Integration & Inference Pipeline

### Objective
Load the trained YOLOv11 model and implement an inference pipeline for single image detection.

### Implementation
The `inference.py` script demonstrates:
- Loading trained YOLOv11 model weights
- Performing object detection on input images
- Returning detected classes, confidence scores, and bounding box coordinates

### Run Inference Pipeline

```bash
python inference.py
```

### Expected Output

```
======================================================================
Task 1: Model Integration & Inference Pipeline
======================================================================
Loading model from models/best.pt...
Model loaded successfully!

Testing inference on: yolo/test/images/2_jpg.rf.7586b04d5d6d11d8c40f62e6c0e03842.jpg
----------------------------------------------------------------------

Image: yolo/test/images/2_jpg.rf.7586b04d5d6d11d8c40f62e6c0e03842.jpg
Number of detections: 2

Detections:
----------------------------------------------------------------------

  Detection 1:
    Class Name: 1000 tk
    Confidence Score: 0.9234
    Bounding Box Coordinates:
      x1: 120.50
      y1: 80.30
      x2: 450.20
      y2: 320.10

  Detection 2:
    Class Name: 200 tk
    Confidence Score: 0.8567
    Bounding Box Coordinates:
      x1: 500.10
      y1: 150.20
      x2: 750.30
      y2: 400.50

Visualization saved as 'inference_output.png'
======================================================================
Task 1 completed successfully!
======================================================================
```

### Submission
- ✅ Python script: `inference.py`
- ✅ Sample output: Printed to console and saved as `inference_output.png`

---

## 🌐 Task 2: REST API Development

### Objective
Develop a REST API using FastAPI to serve the trained model.

### API Endpoints

#### 1. Root Endpoint
```bash
GET http://localhost:8000/
```

#### 2. Health Check
```bash
GET http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "model_status": "loaded"
}
```

#### 3. Predict Endpoint
```bash
POST http://localhost:8000/predict
```

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body:
  - `file`: Image file (JPEG/PNG)
  - `confidence`: (optional) Confidence threshold (0.0-1.0, default: 0.25)

**Response (JSON):**
```json
{
  "success": true,
  "num_detections": 2,
  "detections": [
    {
      "class_name": "1000 tk",
      "confidence": 0.9234,
      "bounding_box": {
        "x1": 120.5,
        "y1": 80.3,
        "x2": 450.2,
        "y2": 320.1
      }
    },
    {
      "class_name": "200 tk",
      "confidence": 0.8567,
      "bounding_box": {
        "x1": 500.1,
        "y1": 150.2,
        "x2": 750.3,
        "y2": 400.5
      }
    }
  ],
  "message": "Detection completed successfully"
}
```

### Start the API Server

```bash
python api.py
```

The API will be available at `http://localhost:8000`

### Interactive API Documentation

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### Error Handling

The API handles errors gracefully:
- **400 Bad Request:** Invalid file type or confidence threshold
- **503 Service Unavailable:** Model not loaded
- **500 Internal Server Error:** Processing errors

### Submission
- ✅ API source code: `api.py`
- ✅ Screenshot/logs: Use Postman or curl (see Task 3)

---

## 🧪 Task 3: API Testing & Validation

### Objective
Test the API using Postman/curl with at least 5 different test images and verify predictions and response format.

### Automated Testing Script

```bash
python test_api.py
```

This script:
- Tests health check endpoint
- Tests `/predict` endpoint with 5+ test images
- Validates response format
- Tests error handling
- Generates summary report

### Manual Testing with cURL

```bash
# Health check
curl http://localhost:8000/health

# Test prediction
curl -X POST "http://localhost:8000/predict" \
  -F "file=@yolo/test/images/2_jpg.rf.7586b04d5d6d11d8c40f62e6c0e03842.jpg" \
  -F "confidence=0.25"
```

### Manual Testing with Postman

1. Open Postman
2. Create new POST request: `http://localhost:8000/predict`
3. Go to **Body** → **form-data**
4. Add key `file` (type: **File**) → Select image
5. Add key `confidence` (type: **Text**) → Value: `0.25`
6. Click **Send**

### Expected Test Output

```
======================================================================
Task 3: API Testing & Validation
======================================================================
Testing with 5 test images
======================================================================

[Test Image 1/5]
Testing with image: 2_jpg.rf.7586b04d5d6d11d8c40f62e6c0e03842.jpg
Status Code: 200
Success: True
Number of Detections: 2
Detections:
  1. Class: 1000 tk
     Confidence: 0.9234
     Bounding Box: (120.50, 80.30) -> (450.20, 320.10)
[OK] Prediction successful and response format verified

...

Test Summary
======================================================================
Total images tested: 5
Total detections: 12
Average detections per image: 2.40

Detections by class:
  100 tk: 2
  1000 tk: 5
  200 tk: 3
  500 tk: 2

Confidence Statistics:
  Average: 0.8234
  Minimum: 0.7123
  Maximum: 0.9456

Brief Discussion on Prediction Accuracy
======================================================================
The model was tested on 5 images and detected 12 total objects.
Average detections per image: 2.40
The confidence scores range from 0.7123 to 0.9456, 
with an average of 0.8234, indicating good model confidence.
```

### Submission
- ✅ Test images: Located in `yolo/test/images/`
- ✅ Screenshots: API requests and responses (Postman/curl)
- ✅ Discussion: Prediction accuracy included in test output

---

## 🐳 Task 4: Dockerization

### Objective
Containerize the entire application using Docker.

### Dockerfile

The `Dockerfile` includes:
- Python 3.11 slim base image
- System dependencies installation
- Python dependencies from `requirements.txt`
- Application code and model weights copying
- Port 8000 exposure
- Health check configuration

### Build Docker Image

```bash
docker build -t taka-note-detector:latest .
```

**Expected Output:**
```
[+] Building ...
...
Successfully built <image-id>
Successfully tagged taka-note-detector:latest
```

### Run Docker Container

**Windows:**
```bash
docker run -d --name taka-detector-api -p 8000:8000 -v "%cd%\models:/app/models" taka-note-detector:latest
```

**Linux/Mac:**
```bash
docker run -d --name taka-detector-api -p 8000:8000 -v "$(pwd)/models:/app/models" taka-note-detector:latest
```

### Verify Container is Running

```bash
docker ps
```

**Expected Output:**
```
CONTAINER ID   IMAGE                      STATUS          PORTS
<id>           taka-note-detector:latest  Up <time>       0.0.0.0:8000->8000/tcp
```

### Check Container Logs

```bash
docker logs taka-detector-api
```

### Test API in Docker

```bash
# Health check
curl http://localhost:8000/health

# Or use test script
python test_api.py
```

### Stop and Remove Container

```bash
docker stop taka-detector-api
docker rm taka-detector-api
```

### Submission
- ✅ Dockerfile: `Dockerfile`
- ✅ requirements.txt: `requirements.txt`
- ✅ Build command: `docker build -t taka-note-detector:latest .`
- ✅ Run command: `docker run -d --name taka-detector-api -p 8000:8000 -v "%cd%\models:/app/models" taka-note-detector:latest`
- ✅ Screenshot/log: Docker container running and API accessible

---

## 📚 Task 5: Deployment & Documentation

### Objective
Write clear documentation explaining how to build Docker image, run container, and use API endpoint.

### Documentation Structure

This README.md includes:
- ✅ Project overview and structure
- ✅ Prerequisites and installation
- ✅ Detailed instructions for each task
- ✅ Usage examples
- ✅ Troubleshooting guide

### Code Quality

All code includes:
- ✅ Well-structured folder hierarchy
- ✅ Clear comments explaining functionality
- ✅ Error handling
- ✅ Type hints where appropriate

### Submission
- ✅ README.md: This comprehensive documentation
- ✅ Complete project folder with:
  - API code (`api.py`)
  - Dockerfile
  - Model weights (in `models/` directory)
  - All documentation

---

## 💡 Usage Examples

### Example 1: Run Inference on Single Image

```python
from inference import TakaNoteDetector

# Initialize detector
detector = TakaNoteDetector(model_path="models/best.pt")

# Perform detection
results = detector.predict("yolo/test/images/test_image.jpg", confidence_threshold=0.25)

# Print results
print(f"Detections: {results['num_detections']}")
for det in results['detections']:
    print(f"  {det['class_name']}: {det['confidence']:.4f}")
```

### Example 2: API Request with Python

```python
import requests

# Test prediction
with open('yolo/test/images/test_image.jpg', 'rb') as f:
    files = {'file': f}
    data = {'confidence': 0.25}
    response = requests.post('http://localhost:8000/predict', files=files, data=data)
    print(response.json())
```

### Example 3: Complete Workflow

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up model weights
copy "runs\detect\currency detection\weights\best.pt" models\best.pt

# 3. Test inference
python inference.py

# 4. Start API (Terminal 1)
python api.py

# 5. Test API (Terminal 2)
python test_api.py

# 6. Docker deployment
docker build -t taka-note-detector:latest .
docker run -d --name taka-detector-api -p 8000:8000 -v "%cd%\models:/app/models" taka-note-detector:latest
```

---

## 🔍 Troubleshooting

### Model Weights Not Found

**Error:** `FileNotFoundError: Model weights not found at models/best.pt`

**Solution:**
1. Ensure model weights are in `models/best.pt`
2. Verify file exists: `dir models\best.pt` (Windows) or `ls models/best.pt` (Linux/Mac)

### API Not Starting

**Error:** `ModuleNotFoundError` or import errors

**Solution:**
1. Install dependencies: `pip install -r requirements.txt`
2. Check Python version: `python --version` (should be 3.11+)

### Port Already in Use

**Error:** `Address already in use`

**Solution:**
1. Change port in `api.py`: `uvicorn.run(..., port=8001)`
2. Or stop the service using port 8000

### Docker Build Fails

**Error:** Build errors or missing files

**Solution:**
1. Ensure all files are in project directory
2. Check Dockerfile paths are correct
3. Verify model weights are available

### Container Not Accessible

**Error:** Connection refused

**Solution:**
1. Check container is running: `docker ps`
2. Check container logs: `docker logs taka-detector-api`
3. Verify port mapping: `-p 8000:8000`

---

## 📊 Project Summary

### Tasks Completed

| Task | Status | Files |
|------|--------|-------|
| Task 1: Inference Pipeline | ✅ | `inference.py` |
| Task 2: REST API | ✅ | `api.py` |
| Task 3: API Testing | ✅ | `test_api.py` |
| Task 4: Dockerization | ✅ | `Dockerfile`, `requirements.txt` |
| Task 5: Documentation | ✅ | `README.md` |

### Key Features

- ✅ YOLOv11 model integration
- ✅ FastAPI REST API with `/predict` endpoint
- ✅ Comprehensive error handling
- ✅ Docker containerization
- ✅ Automated testing script
- ✅ Complete documentation

---

## 📝 Notes

- Model expects images in JPEG/PNG format
- Confidence threshold can be adjusted (0.0 to 1.0)
- API supports CORS for cross-origin requests
- Docker image includes health check
- All code is well-commented and documented

---

## 👤 Author

Module 12 - Phase 2 Assignment  
Bangladeshi Taka Note Detection Model Deployment

---

## 📄 License

This project is for educational purposes as part of the assignment.

---

**Last Updated:** January 2026
=======
# currency-detection
>>>>>>> 7e06c5a96b877bdcba4179c1a2001bf49d706d3b
