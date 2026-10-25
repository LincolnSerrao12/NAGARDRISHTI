# Pothole Detection Web Interface Setup

## Quick Start

### 1. Install Flask (if not already installed)
```bash
pip install flask
```

### 2. Run the Web Server
```bash
python app.py
```

You should see:
```
========================================
🚀 Starting Pothole Detection Web Interface
========================================
📊 Model: runs/yolov8n_pothole/weights/best.pt
🌐 Open http://localhost:5000 in your browser
========================================
```

### 3. Open in Browser
Open your browser and go to:
```
http://localhost:5000
```

## Features

✅ **Drag & Drop Upload** - Easily upload images
✅ **Real-time Detection** - Run inference on your trained model
✅ **Adjustable Confidence** - Slider to change detection threshold (10% - 99%)
✅ **Visual Results** - See bounding boxes on detected potholes
✅ **Detection Stats** - View confidence scores for each detection
✅ **Responsive Design** - Works on desktop and mobile
✅ **Live Feedback** - See loading status and results instantly

## How to Use

1. **Upload an Image**
   - Click the upload area or drag & drop a JPG/PNG image
   - Image preview will show in the right panel

2. **Adjust Confidence Threshold**
   - Lower values (10-30%) = Detect more potholes (may have false positives)
   - Higher values (70-90%) = Only very confident detections
   - Default is 50%

3. **Click "Analyze Image"**
   - The model will run inference on your image
   - Results will show:
     - Image with bounding boxes around detected potholes
     - Total number of potholes found
     - Confidence score for each detection

4. **Clear and Try Another**
   - Click "Clear" to reset and upload a new image

## File Structure

```
POTHOLE DETECTION/
├── app.py                          # Flask server (main app)
├── templates/
│   └── index.html                 # Web interface
├── runs/yolov8n_pothole/
│   └── weights/
│       └── best.pt                # Your trained model
└── WEB_INTERFACE_SETUP.md          # This file
```

## Technical Details

- **Backend**: Flask (Python)
- **Model**: YOLOv8 Nano (best.pt)
- **Frontend**: HTML/CSS/JavaScript
- **Processing**: Real-time inference using ultralytics YOLO

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Model Not Found
Make sure the model path exists:
```
runs/yolov8n_pothole/weights/best.pt
```

### Memory Issues
If running on a low-memory system:
- Reduce image size in the frontend
- Use a smaller batch size
- Close other applications

### Slow Performance
- This is normal on CPU inference (can take 1-5 seconds per image)
- GPU support available if you have CUDA enabled

## Next Steps

- Test with various pothole images
- Evaluate the model's performance
- Adjust confidence threshold based on your needs
- Export model for production deployment

## Stop the Server
Press `Ctrl+C` in the terminal running the Flask app.
