# Quick Start Guide

## 🚀 Get Started in 5 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set Up Model Weights
```bash
# Create models directory
mkdir models

# Copy your trained model from Phase-1
# Windows:
copy "runs\detect\currency detection\weights\best.pt" models\best.pt

# Linux/Mac:
cp "runs/detect/currency detection/weights/best.pt" models/best.pt
```

### Step 3: Test Inference (Task 1)
```bash
python inference.py
```

**Expected:** Shows detections with classes, confidence, bounding boxes

### Step 4: Start API (Task 2)
```bash
python api.py
```

Keep this terminal open! API runs at `http://localhost:8000`

### Step 5: Test API (Task 3)
**In a new terminal:**
```bash
python test_api.py
```

---

## 🐳 Docker Deployment (Task 4)

### Build Image
```bash
docker build -t taka-note-detector:latest .
```

### Run Container
```bash
# Windows
docker run -d --name taka-detector-api -p 8000:8000 -v "%cd%\models:/app/models" taka-note-detector:latest

# Linux/Mac
docker run -d --name taka-detector-api -p 8000:8000 -v "$(pwd)/models:/app/models" taka-note-detector:latest
```

### Test
```bash
curl http://localhost:8000/health
```

---

## 📋 Testing Checklist

- [ ] Dependencies installed
- [ ] Model weights in `models/best.pt`
- [ ] Inference script works (`python inference.py`)
- [ ] API starts (`python api.py`)
- [ ] Health check passes (`curl http://localhost:8000/health`)
- [ ] Test script runs (`python test_api.py`)
- [ ] Docker builds (`docker build -t taka-note-detector:latest .`)
- [ ] Docker container runs (`docker run ...`)

---

## 📸 For Submission Screenshots

1. **Task 1:** `python inference.py` output
2. **Task 2:** Postman/curl API request and response
3. **Task 3:** `python test_api.py` output (5+ images)
4. **Task 4:** Docker build, run, and API test

---

For detailed documentation, see [README.md](README.md)
