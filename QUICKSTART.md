# 🚀 Pothole Detection - Quick Start Guide

## ✅ You Now Have:

- **665 images** (465 training, 133 validation, 67 test)
- **YOLO format labels** (ready for YOLOv8)
- **Configuration file** (`data.yaml`)
- **Training script** (`train_yolo.py`)
- **Detection script** (`detect.py`)

---

## 🎯 What You Can Do Now:

### **Option 1: Train a Model** (Recommended for beginners)

#### Step 1: Install dependencies
```bash
pip install ultralytics torch torchvision opencv-python
```

#### Step 2: Train the model
```bash
python train_yolo.py
```

**What happens:**
- Downloads pre-trained YOLOv8 Nano weights
- Trains for 100 epochs on your pothole dataset
- Saves best model to `runs/pothole_detection/yolov8n_pothole/weights/best.pt`
- Generates training graphs and metrics

**Time estimate:** 10-30 minutes (depends on GPU/CPU)

**Output:**
- `runs/pothole_detection/yolov8n_pothole/` folder with:
  - `weights/best.pt` — Your trained model
  - `results.csv` — Training metrics
  - `confusion_matrix.png` — Performance visualization

---

### **Option 2: Test Detection** (After training)

#### Detect potholes in an image:
```bash
python detect.py path/to/your/image.jpg
```

#### Detect potholes in a video:
```bash
python detect.py path/to/your/video.mp4
```

**Output:**
- `detection_result.jpg` or `detection_result.mp4` with bounding boxes

---

### **Option 3: Advanced Training** (Fine-tune for your use case)

Edit `train_yolo.py` to customize:

```python
results = model.train(
    data='data.yaml',
    epochs=150,           # ← More epochs = better accuracy (takes longer)
    imgsz=640,            # ← Larger = more detail but slower
    batch=16,             # ← Larger = faster but needs more GPU memory
    device=0,             # ← 0=GPU, -1=CPU
    patience=30,          # ← Early stopping patience
)
```

---

### **Option 4: Use Different Model Sizes**

In `train_yolo.py`, change the model:

```python
# Nano (fast, less accurate) - 3.2M parameters
model = YOLO('yolov8n.pt')

# Small (balanced) - 11.2M parameters  
model = YOLO('yolov8s.pt')

# Medium (accurate, slower) - 25.9M parameters
model = YOLO('yolov8m.pt')

# Large (very accurate, much slower) - 43.7M parameters
model = YOLO('yolov8l.pt')
```

**Recommendation:**
- Start with **Nano** for quick prototyping
- Use **Small** for production if GPU available
- Use **Medium/Large** only if you need maximum accuracy

---

### **Option 5: Data Augmentation & Preprocessing**

The dataset is already in YOLO format, but you can enhance it:

```python
# In train_yolo.py, add augmentation:
results = model.train(
    data='data.yaml',
    epochs=100,
    hsv_h=0.015,          # HSV hue augmentation
    hsv_s=0.7,            # HSV saturation augmentation
    hsv_v=0.4,            # HSV value augmentation
    degrees=10,           # Rotation degrees
    translate=0.1,        # Image translation
    scale=0.5,            # Image scaling
    flipud=0.5,           # Flip upside down probability
    fliplr=0.5,           # Flip left-right probability
    mosaic=1.0,           # Mosaic augmentation
)
```

---

### **Option 6: Evaluate Model Performance**

After training, check your model's performance:

```python
from ultralytics import YOLO

model = YOLO('runs/pothole_detection/yolov8n_pothole/weights/best.pt')

# Validate on test set
metrics = model.val()

print(f"mAP50:     {metrics.box.map50}")      # Accuracy at 50% IoU
print(f"mAP50-95:  {metrics.box.map}")        # Average accuracy
print(f"Precision: {metrics.box.mp}")         # True positives / (TP + FP)
print(f"Recall:    {metrics.box.mr}")         # True positives / (TP + FN)
```

---

### **Option 7: Export Model for Deployment**

Convert trained model to different formats:

```python
from ultralytics import YOLO

model = YOLO('runs/pothole_detection/yolov8n_pothole/weights/best.pt')

# Export to ONNX (for cross-platform deployment)
model.export(format='onnx')

# Export to TensorFlow Lite (for mobile/edge devices)
model.export(format='tflite')

# Export to TorchScript (for PyTorch deployment)
model.export(format='torchscript')

# Export to CoreML (for iOS)
model.export(format='coreml')
```

---

## 📊 Dataset Format Breakdown

Your YOLO dataset structure:
```
Pothole.v1-raw.yolov4pytorch/
├── train/
│   ├── image_001.jpg
│   ├── image_001.txt      (YOLO label: <class> <x> <y> <w> <h>)
│   ├── image_002.jpg
│   ├── image_002.txt
│   └── ...
├── valid/
│   ├── image_...jpg
│   ├── image_...txt
│   └── ...
└── test/
    ├── image_...jpg
    ├── image_...txt
    └── ...
```

**YOLO label format example:**
```
0 0.5 0.5 0.2 0.3
└─────────────────
  Class x_center y_center width height
  (all normalized 0-1)
```

---

## 🎓 Common Tasks

### **Split your own data into train/val/test:**
```python
from sklearn.model_selection import train_test_split

images = [...]  # Your image list
train, temp = train_test_split(images, test_size=0.3)
val, test = train_test_split(temp, test_size=0.5)
# train: 70%, val: 15%, test: 15%
```

### **Add more data to existing dataset:**
1. Put new images in a folder
2. Create YOLO labels (use a labeling tool like Roboflow or LabelImg)
3. Copy to `train/`, `valid/`, or `test/` folder
4. Retrain model

### **Use pretrained model without training:**
```python
from ultralytics import YOLO

# Load pretrained YOLOv8 (trained on COCO, not potholes)
model = YOLO('yolov8n.pt')

# Use directly for detection
results = model.predict(source='image.jpg')
```
⚠️ Note: Pretrained model won't detect potholes well—**you need to train on pothole data**

---

## ⚡ Quick Commands Reference

```bash
# Install
pip install ultralytics torch

# Train
python train_yolo.py

# Detect on image
python detect.py image.jpg

# Detect on video
python detect.py video.mp4

# Evaluate
python -c "from ultralytics import YOLO; YOLO('runs/pothole_detection/yolov8n_pothole/weights/best.pt').val()"

# Export to ONNX
python -c "from ultralytics import YOLO; YOLO('runs/pothole_detection/yolov8n_pothole/weights/best.pt').export(format='onnx')"
```

---

## 🔧 Troubleshooting

**Problem: "CUDA out of memory"**
- Solution: Reduce batch size: `batch=4` or `batch=2` in train_yolo.py

**Problem: Training is very slow**
- Solution: Use `device=-1` to check if GPU is being used; if slow on GPU, reduce `imgsz=480`

**Problem: Model not detecting potholes well**
- Solution: Train for more epochs or use larger model (yolov8s instead of yolov8n)

**Problem: No module named 'ultralytics'**
- Solution: `pip install ultralytics`

---

## 📈 Expected Performance

Based on web research with pothole datasets:
- **Precision:** 85-89% (correct detections)
- **Recall:** 80-85% (catching most potholes)
- **mAP50:** 80-88% (overall quality)

Your results may vary based on:
- Model size (Nano < Small < Medium < Large)
- Number of training epochs
- Batch size and learning rate
- Data quality and augmentation

---

## 🎯 Next Steps

1. ✅ **Now:** Run `python train_yolo.py`
2. ⏳ **Wait:** Training completes (10-30 min)
3. 🧪 **Test:** Run `python detect.py image.jpg` on test images
4. 📊 **Evaluate:** Check performance in `runs/pothole_detection/`
5. 🚀 **Deploy:** Export model and integrate into your application

---

Good luck! 🚀
