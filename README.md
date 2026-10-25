# Nagar Drishti 🛣️

AI-powered road-damage detection for smarter city maintenance, built for **Smart India Hackathon (SIH)**.

Nagar Drishti detects potholes in images and video using **YOLOv8** and serves results through a simple **Flask** web app, so authorities can find and prioritise road repairs from data instead of manual inspection.

## Features
- Real-time pothole detection on images and videos (bounding boxes + confidence scores)
- Frame-by-frame video processing for continuous road monitoring
- Lightweight YOLOv8-nano model (~6 MB) that runs on CPU
- Web UI for upload, detection and result viewing

## Tech stack
Python · YOLOv8 (Ultralytics / PyTorch) · OpenCV · Flask · HTML/CSS/JS

## Run locally
```bash
pip install -r requirements.txt
python app.py
```
Then open http://localhost:5000.

## Project layout
| Path | Purpose |
|------|---------|
| `app.py`, `templates/` | Flask web app |
| `detect.py` | Inference script |
| `train_yolo.py` | Model training |
| `data.yaml` | Dataset config (Roboflow pothole dataset, 665 images) |
| `SIH_DEMO_BRIEF.md` | Problem statement, solution and demo notes |

## Team
| Name | GitHub |
|------|--------|
| Lincoln Serrao | [@LincolnSerrao](https://github.com/LincolnSerrao) |
| _Add teammate_ | _@username_ |
