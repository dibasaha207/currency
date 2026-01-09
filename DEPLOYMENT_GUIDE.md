# Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: Local API Deployment (Recommended for Testing)

#### Step 1: Start the API Server

**Windows:**
```bash
# Double-click start_api.bat
# OR
python api.py
```

**Linux/Mac:**
```bash
python api.py
```

You should see:
```
Loading model from models/best.pt...
Model loaded successfully!
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### Step 2: Verify API is Running

**Open a new terminal window** and run:
```bash
python test_api.py
```

Or test manually:
```bash
# Health check
curl http://localhost:8000/health

# Or in browser:
# http://localhost:8000/docs (Interactive API documentation)
```

#### Step 3: Test with Currency Image

**Using Python:**
```bash
python test_api.py
```

**Using Postman:**
1. Open Postman
2. POST → `http://localhost:8000/predict`
3. Body → form-data
4. Add `file` (File) → Select currency image
5. Add `confidence` (Text) → `0.25`
6. Send

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/predict" -F "file=@yolo/test/images/12_jpg.rf.ee46cb554e7f052492f63ddef74c96a8.jpg" -F "confidence=0.25"
```

---

### Option 2: Docker Deployment (Production)

#### Step 1: Build Docker Image

```bash
docker build -t taka-note-detector:latest .
```

**Expected Output:**
```
[+] Building ...
Successfully built <image-id>
Successfully tagged taka-note-detector:latest
```

#### Step 2: Run Docker Container

**Windows:**
```bash
docker run -d --name taka-detector-api -p 8000:8000 -v "%cd%\models:/app/models" taka-note-detector:latest
```

**Linux/Mac:**
```bash
docker run -d --name taka-detector-api -p 8000:8000 -v "$(pwd)/models:/app/models" taka-note-detector:latest
```

#### Step 3: Verify Container is Running

```bash
docker ps
```

**Expected Output:**
```
CONTAINER ID   IMAGE                      STATUS          PORTS
<id>           taka-note-detector:latest  Up <time>       0.0.0.0:8000->8000/tcp
```

#### Step 4: Check Container Logs

```bash
docker logs taka-detector-api
```

#### Step 5: Test API in Docker

```bash
# Health check
curl http://localhost:8000/health

# Or use test script
python test_api.py
```

#### Step 6: Stop Container (when done)

```bash
docker stop taka-detector-api
docker rm taka-detector-api
```

---

## 📋 Deployment Checklist

### Before Deployment:
- [ ] Model weights in `models/best.pt`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Test images available in `yolo/test/images/`

### Local API Deployment:
- [ ] API server started (`python api.py`)
- [ ] Health check passes (`curl http://localhost:8000/health`)
- [ ] Test with currency image successful
- [ ] API documentation accessible (`http://localhost:8000/docs`)

### Docker Deployment:
- [ ] Docker image built successfully
- [ ] Container running (`docker ps`)
- [ ] API accessible from host (`curl http://localhost:8000/health`)
- [ ] Test with currency image successful

---

## 🔧 Troubleshooting

### API Won't Start

**Issue:** Port 8000 already in use

**Solution:**
1. Change port in `api.py`:
   ```python
   uvicorn.run("api:app", host="0.0.0.0", port=8001)
   ```
2. Or stop the service using port 8000

### Model Not Found

**Issue:** `FileNotFoundError: Model weights not found`

**Solution:**
```bash
# Ensure model is in models/best.pt
dir models\best.pt  # Windows
ls models/best.pt   # Linux/Mac
```

### Docker Build Fails

**Issue:** Build errors

**Solution:**
1. Check Dockerfile syntax
2. Ensure all files are in project directory
3. Verify model weights are available

### Container Won't Start

**Issue:** Container exits immediately

**Solution:**
```bash
# Check logs
docker logs taka-detector-api

# Check if model weights are mounted correctly
docker exec taka-detector-api ls /app/models
```

---

## 🌐 Accessing the API

### Local Deployment:
- **API Base URL:** `http://localhost:8000`
- **Health Check:** `http://localhost:8000/health`
- **API Docs:** `http://localhost:8000/docs`
- **Predict Endpoint:** `http://localhost:8000/predict`

### Docker Deployment:
- Same URLs as above (port mapped to host)
- Accessible from any machine on the network (if firewall allows)

---

## 📸 For Submission

Take screenshots of:
1. ✅ API server running (terminal output)
2. ✅ Health check response
3. ✅ Postman/curl request and response
4. ✅ Docker build output
5. ✅ Docker container running (`docker ps`)
6. ✅ API working in Docker

---

## 🎯 Next Steps After Deployment

1. **Test the API** with multiple currency images
2. **Verify all endpoints** work correctly
3. **Check error handling** with invalid inputs
4. **Document any issues** encountered
5. **Take screenshots** for submission

---

**Your API is now deployed and ready to detect Bangladeshi Taka notes!** 🎉
