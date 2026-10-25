"""
YOLOv8 Pothole Detection Training
"""

from ultralytics import YOLO

print("=" * 70)
print("🚀 POTHOLE DETECTION - YOLOv8 TRAINING")
print("=" * 70)

# Load model
print("\n1️⃣ Loading YOLOv8 model...")
model = YOLO('yolov8n.pt')  # nano - fast training

# Train
print("2️⃣ Starting training (this may take 10-30 minutes)...\n")
results = model.train(
    data='data.yaml',
    epochs=50,  # Reduced epochs for CPU (can increase later)
    imgsz=416,  # Smaller image size for CPU
    batch=2,    # Smaller batch for CPU
    device='cpu',  # CPU training (no GPU available)
    patience=10,
    save=True,
    project='runs/pothole_detection',
    name='yolov8n_pothole',
    verbose=True,
)

print("\n" + "=" * 70)
print("✅ Training Complete!")
print("=" * 70)

# Results
print("\n📊 Results:")
print(f"  Best mAP50:     {results.results_dict.get('metrics/mAP50(B)', 'N/A')}")
print(f"  Best mAP50-95:  {results.results_dict.get('metrics/mAP50-95(B)', 'N/A')}")

print("\n📁 Trained model saved to: runs/pothole_detection/yolov8n_pothole/")
print("\n🎯 Next steps:")
print("  1. View results: runs/pothole_detection/yolov8n_pothole/")
print("  2. Test on images: python detect.py")
print("  3. Deploy: Export to ONNX/TensorRT/TFLite")
