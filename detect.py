"""
Detect potholes in images/videos using trained YOLOv8 model
"""

import cv2
from ultralytics import YOLO
import argparse
from pathlib import Path

def detect_potholes(model_path, input_path, confidence=0.5):
    """
    Detect potholes in an image or video

    Args:
        model_path: Path to trained model (e.g., 'runs/pothole_detection/yolov8n_pothole/weights/best.pt')
        input_path: Path to image or video
        confidence: Confidence threshold (0-1)
    """

    # Load model
    print(f"📥 Loading model from: {model_path}")
    model = YOLO(model_path)

    input_file = Path(input_path)

    # Check if input is image or video
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm'}

    if input_file.suffix.lower() in image_extensions:
        print(f"\n🖼️  Detecting potholes in image: {input_path}")
        detect_image(model, input_path, confidence)
    elif input_file.suffix.lower() in video_extensions:
        print(f"\n🎥 Detecting potholes in video: {input_path}")
        detect_video(model, input_path, confidence)
    else:
        print(f"❌ Unsupported file format: {input_file.suffix}")
        print("Supported: jpg, png, bmp, mp4, avi, mov, mkv, webm")

def detect_image(model, image_path, confidence):
    """Detect and display results on image"""
    # Read image
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Could not read image: {image_path}")
        return

    # Predict
    results = model.predict(source=image, conf=confidence)

    # Draw results
    result_image = results[0].plot()

    # Save result
    output_path = f"detection_result.jpg"
    cv2.imwrite(output_path, result_image)
    print(f"✅ Detection complete! Saved to: {output_path}")

    # Print statistics
    if results[0].boxes:
        print(f"   Found {len(results[0].boxes)} pothole(s)")
        for i, box in enumerate(results[0].boxes):
            conf = box.conf.item()
            print(f"   - Pothole {i+1}: confidence {conf:.2%}")
    else:
        print("   No potholes detected")

def detect_video(model, video_path, confidence):
    """Detect potholes in video and save result"""
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Setup output video
    output_path = "detection_result.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0
    detection_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Predict
        results = model.predict(source=frame, conf=confidence, verbose=False)

        # Draw
        result_frame = results[0].plot()
        out.write(result_frame)

        frame_count += 1
        detection_count += sum(1 for _ in results[0].boxes) if results[0].boxes else 0

        if frame_count % 30 == 0:
            print(f"  Processed {frame_count} frames...")

    cap.release()
    out.release()

    print(f"\n✅ Video detection complete!")
    print(f"   Frames processed: {frame_count}")
    print(f"   Total detections: {detection_count}")
    print(f"   Saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Detect potholes in images/videos')
    parser.add_argument('input', help='Path to image or video')
    parser.add_argument('--model', default='runs/pothole_detection/yolov8n_pothole/weights/best.pt',
                       help='Path to trained model')
    parser.add_argument('--confidence', type=float, default=0.5,
                       help='Confidence threshold (0-1)')

    args = parser.parse_args()

    detect_potholes(args.model, args.input, args.confidence)
