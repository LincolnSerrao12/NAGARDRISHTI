"""
Automated Pothole Detection Training Pipeline
Handles: dataset download → annotation conversion → model training → evaluation
"""

import os
import sys
import subprocess
from pathlib import Path
from PIL import Image
from ultralytics import YOLO
import time
from datetime import datetime

class PotholeTrainingPipeline:
    def __init__(self):
        self.project_dir = Path.cwd()
        self.dataset_dir = self.project_dir / "Pothole.v1-raw.yolov4pytorch"
        self.runs_dir = self.project_dir / "runs" / "pothole_detection"
        self.log_file = self.project_dir / "training_log.txt"

    def log(self, message):
        """Log messages to console and file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_msg + "\n")

    def check_dataset(self):
        """Check if dataset exists"""
        self.log("=" * 70)
        self.log("STEP 1: Checking dataset...")
        self.log("=" * 70)

        if not self.dataset_dir.exists():
            self.log("❌ Dataset not found! Please download first:")
            self.log("   python download_simple.py YOUR_API_KEY")
            return False

        # Check train/valid/test folders
        for split in ['train', 'valid', 'test']:
            split_path = self.dataset_dir / split
            if not split_path.exists():
                self.log(f"❌ {split} folder not found!")
                return False

            images = list(split_path.glob('*.jpg'))
            self.log(f"✅ {split}: {len(images)} images")

        return True

    def convert_annotations(self):
        """Convert Pascal VOC annotations to YOLO format"""
        self.log("\n" + "=" * 70)
        self.log("STEP 2: Converting annotations (VOC → YOLO)...")
        self.log("=" * 70)

        for split in ['train', 'valid', 'test']:
            split_path = self.dataset_dir / split
            annotations_file = split_path / '_annotations.txt'

            if not annotations_file.exists():
                self.log(f"⚠️  {split}/_annotations.txt not found, skipping")
                continue

            self.log(f"📝 Processing {split} annotations...")

            with open(annotations_file, 'r') as f:
                lines = f.readlines()

            converted = 0
            skipped = 0

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                parts = line.split()
                image_filename = parts[0]
                image_path = split_path / image_filename

                # Check if label already exists
                label_filename = image_filename.rsplit('.', 1)[0] + '.txt'
                label_path = split_path / label_filename

                if label_path.exists():
                    skipped += 1
                    continue

                # Get image dimensions
                try:
                    img = Image.open(image_path)
                    width, height = img.size
                except Exception as e:
                    self.log(f"  ⚠️  Could not read {image_filename}: {e}")
                    continue

                # Convert annotations
                yolo_annots = self.voc_to_yolo(line, width, height)

                # Write YOLO format label file
                with open(label_path, 'w') as f:
                    for annot in yolo_annots:
                        f.write(annot + '\n')

                converted += 1

            total = converted + skipped
            self.log(f"  ✅ {split}: {converted} new + {skipped} existing = {total} labels")

        self.log("✅ Annotation conversion complete!")
        return True

    @staticmethod
    def voc_to_yolo(voc_line, img_width, img_height):
        """Convert VOC to YOLO format"""
        yolo_annots = []
        parts = voc_line.split()

        coords = parts[1:]
        for coord_str in coords:
            x1, y1, x2, y2, class_id = map(float, coord_str.split(','))

            center_x = (x1 + x2) / 2 / img_width
            center_y = (y1 + y2) / 2 / img_height
            width = (x2 - x1) / img_width
            height = (y2 - y1) / img_height

            center_x = max(0, min(1, center_x))
            center_y = max(0, min(1, center_y))
            width = max(0, min(1, width))
            height = max(0, min(1, height))

            yolo_annots.append(f"{int(class_id)} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}")

        return yolo_annots

    def verify_data_yaml(self):
        """Create/verify data.yaml"""
        self.log("\n" + "=" * 70)
        self.log("STEP 3: Verifying data configuration...")
        self.log("=" * 70)

        data_yaml_path = self.project_dir / "data.yaml"

        yaml_content = f"""path: {str(self.dataset_dir)}
train: train
val: valid
test: test

nc: 1
names: ['pothole']
"""

        with open(data_yaml_path, 'w') as f:
            f.write(yaml_content)

        self.log(f"✅ data.yaml created at: {data_yaml_path}")
        return str(data_yaml_path)

    def train_model(self):
        """Train YOLOv8 model"""
        self.log("\n" + "=" * 70)
        self.log("STEP 4: Training YOLOv8 Model...")
        self.log("=" * 70)

        try:
            self.log("📥 Loading YOLOv8n model...")
            model = YOLO('yolov8n.pt')

            data_yaml = str(self.project_dir / "data.yaml")

            self.log("🚀 Starting training (this will take 2-4 hours on CPU)...")
            self.log("   Epochs: 50")
            self.log("   Batch size: 2")
            self.log("   Device: CPU")

            results = model.train(
                data=data_yaml,
                epochs=50,
                imgsz=416,
                batch=2,
                device='cpu',
                patience=10,
                save=True,
                project=str(self.runs_dir.parent),
                name='yolov8n_pothole',
                verbose=False,
            )

            self.log("\n✅ Training complete!")
            return results

        except Exception as e:
            self.log(f"❌ Training failed: {e}")
            return None

    def evaluate_model(self, results):
        """Evaluate trained model"""
        self.log("\n" + "=" * 70)
        self.log("STEP 5: Evaluating Model...")
        self.log("=" * 70)

        try:
            best_model_path = self.runs_dir / "yolov8n_pothole" / "weights" / "best.pt"

            if not best_model_path.exists():
                self.log(f"❌ Best model not found at {best_model_path}")
                return False

            self.log(f"📥 Loading best model from: {best_model_path}")
            model = YOLO(str(best_model_path))

            self.log("🔍 Running validation...")
            metrics = model.val()

            self.log("\n📊 Model Performance:")
            self.log(f"   mAP50:    {metrics.box.map50:.3f}")
            self.log(f"   mAP50-95: {metrics.box.map:.3f}")
            self.log(f"   Precision: {metrics.box.mp:.3f}")
            self.log(f"   Recall:    {metrics.box.mr:.3f}")

            return True

        except Exception as e:
            self.log(f"⚠️  Evaluation failed: {e}")
            return False

    def generate_summary(self):
        """Generate training summary"""
        self.log("\n" + "=" * 70)
        self.log("✅ TRAINING PIPELINE COMPLETE!")
        self.log("=" * 70)

        best_model = self.runs_dir / "yolov8n_pothole" / "weights" / "best.pt"
        if best_model.exists():
            self.log(f"\n🎯 Trained model saved to:")
            self.log(f"   {best_model}")

        self.log("\n📊 Training results saved to:")
        self.log(f"   {self.runs_dir / 'yolov8n_pothole'}/")

        self.log("\n🚀 Next steps:")
        self.log("   1. Test on image: python detect.py image.jpg")
        self.log("   2. Test on video: python detect.py video.mp4")
        self.log("   3. Export model: python -c \"from ultralytics import YOLO; YOLO('runs/pothole_detection/yolov8n_pothole/weights/best.pt').export(format='onnx')\"")

        self.log(f"\n📋 Full log saved to: {self.log_file}")

    def run(self):
        """Run complete pipeline"""
        start_time = time.time()

        self.log("\n")
        self.log("🤖 POTHOLE DETECTION - AUTOMATED TRAINING PIPELINE")
        self.log(f"   Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Step 1: Check dataset
        if not self.check_dataset():
            self.log("\n❌ Pipeline failed: Dataset not ready")
            return False

        # Step 2: Convert annotations
        if not self.convert_annotations():
            self.log("\n❌ Pipeline failed: Annotation conversion error")
            return False

        # Step 3: Verify config
        self.verify_data_yaml()

        # Step 4: Train model
        results = self.train_model()
        if results is None:
            self.log("\n❌ Pipeline failed: Training error")
            return False

        # Step 5: Evaluate
        self.evaluate_model(results)

        # Summary
        self.generate_summary()

        elapsed = time.time() - start_time
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        self.log(f"\n⏱️  Total time: {hours}h {minutes}m")

        return True

if __name__ == "__main__":
    pipeline = PotholeTrainingPipeline()
    success = pipeline.run()
    sys.exit(0 if success else 1)
