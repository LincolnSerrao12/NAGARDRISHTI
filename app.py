"""
Flask web app for Pothole Detection using trained YOLOv8 model
"""

from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from ultralytics import YOLO
import cv2
import os
from pathlib import Path
import base64
from io import BytesIO
import numpy as np
import tempfile
import uuid
import imageio
import mimetypes
from urllib.parse import quote

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Add CORS headers support
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Load the trained model
# Try multiple model path options
model_paths = [
    'runs/detect/runs/pothole_detection/yolov8n_pothole-2/weights/best.pt',
    'runs/detect/train-3/weights/best.pt',
    'runs/detect/train-2/weights/best.pt',
    'runs/yolov8n_pothole/weights/best.pt'
]

MODEL_PATH = None
for path in model_paths:
    if os.path.exists(path):
        MODEL_PATH = path
        break

if MODEL_PATH is None:
    print("⚠️  Warning: No trained model found at expected locations")
    print(f"Searched paths: {model_paths}")
    MODEL_PATH = model_paths[0]  # Use first path as default

print(f"Loading model from: {MODEL_PATH}")
model = YOLO(MODEL_PATH)
print("✅ Model loaded successfully!")

@app.route('/')
def index():
    return render_template('index.html')

def process_video(video_path, confidence):
    """Process video file with object tracking to count unique potholes"""
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")

    try:
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0 or fps is None:
            fps = 30
            print(f"[WARNING] FPS not detected, using default: {fps}")

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if width == 0 or height == 0:
            raise ValueError(f"Invalid video dimensions: {width}x{height}")

        output_uuid = str(uuid.uuid4())
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], f'output_{output_uuid}.mp4')

        print(f"[VIDEO] ==========================================")
        print(f"[VIDEO] Input: {video_path}")
        print(f"[VIDEO] Output: {output_path}")
        print(f"[VIDEO] Resolution: {width}x{height}")
        print(f"[VIDEO] FPS: {fps}")
        print(f"[VIDEO] Total Frames: {total_frames}")
        print(f"[VIDEO] Using Object Tracking (ByteTrack)")
        print(f"[VIDEO] ==========================================")

        frame_count = 0
        unique_pothole_ids = set()
        all_detections = []
        processed_frames = []

        print(f"[VIDEO] Starting frame processing with tracking...")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            progress = int((frame_count / total_frames) * 100) if total_frames > 0 else 0

            if frame_count % max(1, total_frames // 10) == 0 or frame_count <= 5:
                print(f"[VIDEO] Frame {frame_count}/{total_frames} ({progress}%)")

            # Run tracking on frame (ByteTrack automatically assigned IDs)
            results = model.track(source=frame, conf=confidence, verbose=False, persist=True)

            # Draw results on frame with track IDs
            result_frame = results[0].plot()

            # Track unique potholes by their track ID
            if results[0].boxes and results[0].boxes.id is not None:
                try:
                    track_ids = results[0].boxes.id.cpu().numpy()
                    for i, track_id in enumerate(track_ids):
                        conf = float(results[0].boxes.conf[i].item())
                        track_id_int = int(track_id)
                        unique_pothole_ids.add(track_id_int)
                        all_detections.append({
                            'track_id': track_id_int,
                            'frame': frame_count,
                            'confidence': f'{conf:.2%}',
                            'confidence_value': conf
                        })
                except Exception as e:
                    print(f"[WARNING] Error tracking potholes on frame {frame_count}: {e}")

            # Convert BGR to RGB for imageio
            result_frame_rgb = cv2.cvtColor(result_frame, cv2.COLOR_BGR2RGB)
            processed_frames.append(result_frame_rgb)

        cap.release()
        unique_pothole_count = len(unique_pothole_ids)
        print(f"[VIDEO] ✅ Processed {frame_count} frames")
        print(f"[VIDEO] Unique potholes tracked: {unique_pothole_count}")

        # Write frames to MP4 using imageio with ffmpeg backend
        print(f"[VIDEO] Encoding to MP4... (writing {len(processed_frames)} frames)")
        try:
            writer = imageio.get_writer(output_path, fps=fps, codec='libx264', pixelformat='yuv420p')
            for i, frame in enumerate(processed_frames):
                writer.append_data(frame)
                if (i + 1) % max(1, len(processed_frames) // 10) == 0:
                    print(f"[VIDEO] Encoded {i + 1}/{len(processed_frames)} frames")
            writer.close()
            print(f"[VIDEO] ✅ MP4 encoding completed successfully")
        except Exception as e:
            print(f"[ERROR] Failed to write MP4: {str(e)}")
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except:
                    pass
            raise ValueError(f"Failed to encode video: {str(e)}")

        # Verify the output file was created
        if not os.path.exists(output_path):
            raise ValueError(f"Output video file was not created: {output_path}")

        file_size = os.path.getsize(output_path)
        if file_size == 0:
            raise ValueError(f"Output video file is empty (0 bytes): {output_path}")

        print(f"[VIDEO] ✅ ==========================================")
        print(f"[VIDEO] Processing Complete!")
        print(f"[VIDEO] File: {output_path}")
        print(f"[VIDEO] Size: {file_size / (1024*1024):.2f} MB")
        print(f"[VIDEO] Unique Potholes: {unique_pothole_count}")
        print(f"[VIDEO] ✅ ==========================================")

        return output_path, unique_pothole_count, all_detections

    except Exception as e:
        cap.release()
        print(f"[ERROR] Video processing failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

@app.route('/detect', methods=['POST'])
def detect():
    try:
        confidence = float(request.form.get('confidence', 0.5))

        # Check if image or video file is present
        if 'image' not in request.files and 'video' not in request.files:
            return jsonify({'error': 'No image or video provided'}), 400

        file = None
        is_video = False

        if 'image' in request.files:
            file = request.files['image']
        else:
            file = request.files['video']
            is_video = True

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Save uploaded file temporarily
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()) + '_' + file.filename)
        file.save(temp_path)

        if is_video:
            # Process video
            print(f"Processing video file: {file.filename}")
            output_path, total_detected, detections = process_video(temp_path, confidence)

            # Extract video ID from path - FIX: Properly handle .mp4 extension
            video_filename = os.path.basename(output_path)  # e.g., "output_xxxxx.mp4"
            video_id = video_filename.replace('output_', '').replace('.mp4', '')

            try:
                # Verify file exists before sending response
                if not os.path.exists(output_path):
                    raise ValueError(f"Output video file not found at: {output_path}")

                file_size = os.path.getsize(output_path)
                print(f"[OK] Video processed and saved: {output_path}")
                print(f"[OK] File size: {file_size} bytes")
                print(f"[OK] Video ID: {video_id}")

                # Return JSON with video URL and download URL
                return jsonify({
                    'success': True,
                    'video_url': f'/video/{video_id}',
                    'download_url': f'/download/{video_id}',
                    'total_detected': total_detected,
                    'type': 'video'
                })

            except Exception as e:
                print(f"[ERROR] Error processing video response: {str(e)}")
                import traceback
                traceback.print_exc()
                return jsonify({'error': f'Failed to process video: {str(e)}'}), 500
            finally:
                # Clean up temp input file only (keep output)
                try:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                        print(f"[OK] Cleaned up temp input file: {temp_path}")
                except Exception as e:
                    print(f"[WARNING] Could not clean up temp file: {str(e)}")
        else:
            # Process image - read from temp path since we already saved it
            print(f"Processing image file: {file.filename}")
            image = cv2.imread(temp_path)

            if image is None:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                return jsonify({'error': 'Invalid image file'}), 400

            # Run detection
            print(f"Running detection with confidence: {confidence}")
            results = model.predict(source=image, conf=confidence, verbose=False)

            # Draw results
            result_image = results[0].plot()

            # Convert to base64 for display
            _, buffer = cv2.imencode('.jpg', result_image)
            img_base64 = base64.b64encode(buffer).decode()

            # Extract detection info
            detections = []
            if results[0].boxes:
                for i, box in enumerate(results[0].boxes):
                    conf = float(box.conf.item())
                    detections.append({
                        'id': i + 1,
                        'confidence': f'{conf:.2%}',
                        'confidence_value': conf
                    })

            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)

            return jsonify({
                'success': True,
                'image': f'data:image/jpeg;base64,{img_base64}',
                'detections': detections,
                'total_detected': len(detections),
                'type': 'image'
            })

    except Exception as e:
        print(f"Error: {str(e)}")
        # Clean up on error
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({'error': str(e)}), 500

@app.route('/video/<video_id>', methods=['GET'])
def serve_video(video_id):
    """Serve video file for streaming with proper headers"""
    try:
        # Validate video_id to prevent path traversal attacks
        if not video_id or '..' in video_id or '/' in video_id:
            return jsonify({'error': 'Invalid video ID'}), 400

        # Find the video file
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], f'output_{video_id}.mp4')

        # Extra validation
        if not os.path.isabs(video_path):
            video_path = os.path.abspath(video_path)

        if not os.path.exists(video_path):
            print(f"[ERROR] Video not found: {video_path}")
            return jsonify({'error': f'Video not found. Looked for: {video_path}'}), 404

        file_size = os.path.getsize(video_path)
        print(f"[STREAM] Serving video: {video_path} ({file_size} bytes)")

        return send_file(
            video_path,
            mimetype='video/mp4',
            as_attachment=False,
            download_name=f'pothole_detection_{video_id}.mp4'
        )
    except Exception as e:
        print(f"[ERROR] Video streaming error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/download/<video_id>', methods=['GET'])
def download_video(video_id):
    """Download video file with attachment headers"""
    try:
        # Validate video_id to prevent path traversal attacks
        if not video_id or '..' in video_id or '/' in video_id:
            return jsonify({'error': 'Invalid video ID'}), 400

        video_path = os.path.join(app.config['UPLOAD_FOLDER'], f'output_{video_id}.mp4')

        if not os.path.exists(video_path):
            print(f"[ERROR] Video not found for download: {video_path}")
            return jsonify({'error': 'Video not found'}), 404

        file_size = os.path.getsize(video_path)
        print(f"[DOWNLOAD] Downloading video: {video_path} ({file_size} bytes)")

        return send_file(
            video_path,
            mimetype='video/mp4',
            as_attachment=True,
            download_name=f'pothole_detection_{video_id}.mp4'
        )
    except Exception as e:
        print(f"[ERROR] Video download error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'model': 'loaded'})

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Starting Pothole Detection Web Interface")
    print("=" * 60)
    print(f"📊 Model: {MODEL_PATH}")
    print("🌐 Open http://localhost:5000 in your browser")
    print("=" * 60)
    app.run(debug=False, host='0.0.0.0', port=5000)
