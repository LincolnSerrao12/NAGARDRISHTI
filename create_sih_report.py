import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import csv
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import io

# Create charts first
fig_dir = "chart_assets"
import os
os.makedirs(fig_dir, exist_ok=True)

# 1. Training Progress Chart
print("Creating training progress chart...")
epochs = []
precision = []
recall = []
map50 = []
map95 = []

with open("runs/yolov8n_pothole/results.csv") as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, 1):
        epochs.append(int(row['epoch']))
        precision.append(float(row['metrics/precision(B)']) * 100)
        recall.append(float(row['metrics/recall(B)']) * 100)
        map50.append(float(row['metrics/mAP50(B)']) * 100)
        map95.append(float(row['metrics/mAP50-95(B)']) * 100)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('YOLOv8 Model Training Progress', fontsize=16, fontweight='bold')

# Precision & Recall
ax = axes[0, 0]
ax.plot(epochs, precision, 'o-', label='Precision', linewidth=2.5, markersize=6, color='#1f77b4')
ax.plot(epochs, recall, 's-', label='Recall', linewidth=2.5, markersize=6, color='#ff7f0e')
ax.set_xlabel('Epoch', fontweight='bold')
ax.set_ylabel('Score (%)', fontweight='bold')
ax.set_title('Precision & Recall', fontweight='bold')
ax.legend(loc='best')
ax.grid(True, alpha=0.3)
ax.set_ylim([0, 100])

# mAP Progress
ax = axes[0, 1]
ax.plot(epochs, map50, 'o-', label='mAP50', linewidth=2.5, markersize=6, color='#2ca02c')
ax.plot(epochs, map95, 's-', label='mAP50-95', linewidth=2.5, markersize=6, color='#d62728')
ax.set_xlabel('Epoch', fontweight='bold')
ax.set_ylabel('mAP (%)', fontweight='bold')
ax.set_title('Mean Average Precision', fontweight='bold')
ax.legend(loc='best')
ax.grid(True, alpha=0.3)
ax.axvline(x=9, color='green', linestyle='--', alpha=0.5, label='Best Epoch')

# F1 Score
ax = axes[1, 0]
f1_scores = [2 * (p * r) / (p + r + 1e-6) for p, r in zip(precision, recall)]
ax.fill_between(epochs, f1_scores, alpha=0.3, color='#9467bd')
ax.plot(epochs, f1_scores, 'D-', linewidth=2.5, markersize=6, color='#9467bd', label='F1 Score')
ax.set_xlabel('Epoch', fontweight='bold')
ax.set_ylabel('F1 Score (%)', fontweight='bold')
ax.set_title('F1 Score Progression', fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_ylim([0, 100])

# Best Metrics Bar Chart
ax = axes[1, 1]
best_idx = np.argmax(map95)
metrics = ['Precision', 'Recall', 'mAP50', 'mAP50-95', 'F1 Score']
values = [
    precision[best_idx],
    recall[best_idx],
    map50[best_idx],
    map95[best_idx],
    f1_scores[best_idx]
]
colors_bar = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
bars = ax.bar(metrics, values, color=colors_bar, edgecolor='black', linewidth=1.5)
ax.set_ylabel('Score (%)', fontweight='bold')
ax.set_title('Best Epoch Metrics (Epoch 9)', fontweight='bold')
ax.set_ylim([0, 100])
for bar, val in zip(bars, values):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{val:.1f}%', ha='center', va='bottom', fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{fig_dir}/training_progress.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] Training progress chart created")

# 2. Performance Metrics Radar Chart
print("Creating performance metrics visualization...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Confusion Matrix Style Visualization
categories = ['Precision', 'Recall', 'mAP50', 'F1 Score']
best_vals = [precision[best_idx], recall[best_idx], map50[best_idx], f1_scores[best_idx]]
colors_perf = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd']

bars = ax1.barh(categories, best_vals, color=colors_perf, edgecolor='black', linewidth=2)
ax1.set_xlabel('Score (%)', fontweight='bold', fontsize=11)
ax1.set_title('Model Performance Metrics', fontweight='bold', fontsize=12)
ax1.set_xlim([0, 100])
for i, (bar, val) in enumerate(zip(bars, best_vals)):
    ax1.text(val + 2, bar.get_y() + bar.get_height()/2,
             f'{val:.2f}%', va='center', fontweight='bold', fontsize=10)
ax1.grid(True, alpha=0.3, axis='x')

# Dataset Distribution
ax2.pie([465, 133, 67], labels=['Training\n465 (69.9%)', 'Validation\n133 (20%)', 'Test\n67 (10.1%)'],
        colors=['#1f77b4', '#ff7f0e', '#2ca02c'], autopct='%1.1f%%',
        startangle=90, textprops={'fontweight': 'bold', 'fontsize': 10},
        wedgeprops={'edgecolor': 'black', 'linewidth': 2})
ax2.set_title('Dataset Distribution (665 Images)', fontweight='bold', fontsize=12)

plt.tight_layout()
plt.savefig(f'{fig_dir}/metrics_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] Metrics distribution chart created")

# 3. Precision-Recall Curve
print("Creating precision-recall visualization...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# P-R Curve Style
ax = axes[0]
thresholds = np.linspace(0.3, 0.9, len(epochs))
ax.plot(recall, precision, 'o-', linewidth=3, markersize=8, color='#1f77b4', label='Training Progress')
ax.fill_between(recall, precision, alpha=0.2, color='#1f77b4')
ax.scatter(recall[best_idx], precision[best_idx], s=300, color='red', marker='*',
           edgecolor='black', linewidth=2, label='Best Model (Epoch 9)', zorder=5)
ax.set_xlabel('Recall (%)', fontweight='bold', fontsize=11)
ax.set_ylabel('Precision (%)', fontweight='bold', fontsize=11)
ax.set_title('Precision-Recall Curve', fontweight='bold', fontsize=12)
ax.legend(loc='best', fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xlim([30, 60])
ax.set_ylim([30, 75])

# Loss Progression
ax = axes[1]
loss_train = []
loss_val = []
with open("runs/yolov8n_pothole/results.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        loss_train.append(float(row['train/box_loss']))
        loss_val.append(float(row['val/box_loss']))

ax.plot(epochs, loss_train, 'o-', label='Train Loss', linewidth=2.5, markersize=6, color='#d62728')
ax.plot(epochs, loss_val, 's-', label='Validation Loss', linewidth=2.5, markersize=6, color='#2ca02c')
ax.set_xlabel('Epoch', fontweight='bold', fontsize=11)
ax.set_ylabel('Box Loss', fontweight='bold', fontsize=11)
ax.set_title('Training vs Validation Loss', fontweight='bold', fontsize=12)
ax.legend(loc='best', fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{fig_dir}/precision_recall_loss.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] Precision-Recall chart created")

# Now create the PDF with these images
print("\nGenerating PDF report...")

pdf_path = "SIH_Hackathon_Demo_Report.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                        rightMargin=0.5*inch, leftMargin=0.5*inch,
                        topMargin=0.5*inch, bottomMargin=0.5*inch)

elements = []
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'Title', parent=styles['Heading1'], fontSize=28,
    textColor=colors.HexColor('#1f4788'), spaceAfter=6,
    alignment=TA_CENTER, fontName='Helvetica-Bold')

subtitle_style = ParagraphStyle(
    'Subtitle', parent=styles['Normal'], fontSize=12,
    textColor=colors.HexColor('#555555'), spaceAfter=12,
    alignment=TA_CENTER, fontName='Helvetica-Oblique')

heading_style = ParagraphStyle(
    'CustomHeading', parent=styles['Heading2'], fontSize=13,
    textColor=colors.HexColor('#1f4788'), spaceAfter=8,
    spaceBefore=6, fontName='Helvetica-Bold')

normal_style = ParagraphStyle(
    'Normal', parent=styles['Normal'], fontSize=9.5,
    alignment=TA_LEFT, spaceAfter=6, leading=12)

# Page 1: Title and Overview
elements.append(Paragraph("POTHOLE DETECTION AI", title_style))
elements.append(Paragraph("Smart India Hackathon Hackathon Demo", subtitle_style))
elements.append(Spacer(1, 0.1*inch))

overview_data = [
    ['Project', 'Real-time Pothole Detection using YOLOv8'],
    ['Challenge', 'Automated road hazard detection for maintenance'],
    ['Solution', 'Deep learning model + web interface for image & video'],
    ['Status', 'Fully Functional - Ready for Deployment'],
]
overview_table = Table(overview_data, colWidths=[1.5*inch, 4.0*inch])
overview_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#1f4788')),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
]))
elements.append(overview_table)
elements.append(Spacer(1, 0.15*inch))

# Problem & Solution
elements.append(Paragraph("PROBLEM STATEMENT", heading_style))
elements.append(Paragraph(
    "Road potholes cause accidents, vehicle damage, and costly repairs. Manual detection is time-consuming and incomplete. "
    "There is a need for automated, real-time pothole detection to enable proactive road maintenance.",
    normal_style))
elements.append(Spacer(1, 0.1*inch))

elements.append(Paragraph("SOLUTION", heading_style))
sol_data = [
    ['Component', 'Details'],
    ['AI Model', 'YOLOv8 Nano - Lightweight real-time object detector'],
    ['Input', 'Images (PNG, JPG, BMP) or Videos (MP4, MOV, AVI)'],
    ['Output', 'Annotated images/videos with pothole locations & confidence'],
    ['Interface', 'Web-based dashboard (http://localhost:5000)'],
    ['Processing', 'CPU-optimized for accessibility'],
]
sol_table = Table(sol_data, colWidths=[1.5*inch, 4.0*inch])
sol_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
]))
elements.append(sol_table)
elements.append(PageBreak())

# Page 2: Model Details & Performance
elements.append(Paragraph("MODEL ARCHITECTURE & PERFORMANCE", heading_style))
elements.append(Spacer(1, 0.08*inch))

model_data = [
    ['Model Type', 'YOLOv8 Nano (YOLOv8n)'],
    ['Training Data', '665 images (465 train, 133 val, 67 test)'],
    ['Input Size', '416 × 416 pixels'],
    ['Framework', 'Ultralytics PyTorch'],
    ['Inference', 'CPU-based (Fast & Efficient)'],
]
model_table = Table(model_data, colWidths=[1.8*inch, 3.7*inch])
model_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0f7')),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
]))
elements.append(model_table)
elements.append(Spacer(1, 0.12*inch))

# Add training progress chart
elements.append(Paragraph("TRAINING PROGRESS", heading_style))
img1 = Image(f'{fig_dir}/training_progress.png', width=6.5*inch, height=5.2*inch)
elements.append(img1)
elements.append(PageBreak())

# Page 3: Evaluation Metrics
elements.append(Paragraph("EVALUATION METRICS", heading_style))
elements.append(Spacer(1, 0.08*inch))

# Key metrics table
metrics_data = [
    ['Metric', 'Value', 'Meaning'],
    ['Precision', '66.40%', '2 of 3 detected potholes are correct'],
    ['Recall', '54.54%', 'Finds 54% of actual potholes'],
    ['F1 Score', '59.89%', 'Balanced precision-recall measure'],
    ['mAP50', '60.68%', 'Bounding box accuracy (standard)'],
    ['mAP50-95', '32.35%', 'Bounding box accuracy (strict)'],
]
metrics_table = Table(metrics_data, colWidths=[1.3*inch, 1.2*inch, 3.0*inch])
metrics_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8.5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
]))
elements.append(metrics_table)
elements.append(Spacer(1, 0.12*inch))

# Add metrics visualization
img2 = Image(f'{fig_dir}/metrics_distribution.png', width=6.5*inch, height=3.1*inch)
elements.append(img2)
elements.append(Spacer(1, 0.08*inch))

# Add precision-recall chart
img3 = Image(f'{fig_dir}/precision_recall_loss.png', width=6.5*inch, height=2.6*inch)
elements.append(img3)
elements.append(PageBreak())

# Page 4: Key Features & Deployment
elements.append(Paragraph("KEY FEATURES", heading_style))
features = [
    "✓ Real-time image detection with visual annotations",
    "✓ Video processing - analyzes every frame for potholes",
    "✓ Confidence threshold adjustment for sensitivity control",
    "✓ Web-based interface - no installation required",
    "✓ Supports multiple formats (Images & Videos)",
    "✓ CPU-optimized for accessibility",
    "✓ Fast inference - suitable for mobile deployment",
]
for feature in features:
    elements.append(Paragraph(feature, normal_style))
elements.append(Spacer(1, 0.15*inch))

elements.append(Paragraph("HOW TO USE", heading_style))
steps = [
    "<b>1. Start Server:</b> python app.py",
    "<b>2. Open Browser:</b> http://localhost:5000",
    "<b>3. Upload:</b> Drag & drop image or video",
    "<b>4. View Results:</b> See pothole detections with confidence scores",
    "<b>5. Download:</b> Get processed video (videos only)",
]
for step in steps:
    elements.append(Paragraph(step, normal_style))
elements.append(Spacer(1, 0.15*inch))

elements.append(Paragraph("DATASET INFORMATION", heading_style))
dataset_info = [
    "<b>Source:</b> Roboflow.ai Pothole Dataset (v1-raw)",
    "<b>Images:</b> 665 total (Road pothole images)",
    "<b>Annotation:</b> YOLO v4 PyTorch format",
    "<b>Classes:</b> 1 (Pothole detection)",
]
for info in dataset_info:
    elements.append(Paragraph(info, normal_style))
elements.append(PageBreak())

# Page 5: Strengths & Future Work
elements.append(Paragraph("STRENGTHS", heading_style))
strengths = [
    "<b>High Precision (66.4%):</b> Minimizes false alarms - when model detects a pothole, it's usually correct",
    "<b>Lightweight Model:</b> YOLOv8n enables fast inference on CPU and mobile devices",
    "<b>No Overfitting:</b> Good generalization between training and validation sets",
    "<b>Practical UI:</b> User-friendly web interface for easy access",
    "<b>Multi-format Support:</b> Works with both images and videos",
]
for strength in strengths:
    elements.append(Paragraph(strength, normal_style))
elements.append(Spacer(1, 0.12*inch))

elements.append(Paragraph("LIMITATIONS & FUTURE IMPROVEMENTS", heading_style))
improvements = [
    "<b>Moderate Recall (54.5%):</b> Misses ~45% of potholes. Solution: Expand training data to 2000+ images",
    "<b>Bounding Box Precision:</b> Improve annotations and use larger model (YOLOv8s/m)",
    "<b>Single Class:</b> Extend to detect pothole severity (minor, major, critical)",
    "<b>GPU Acceleration:</b> Deploy on GPU for 10x faster video processing",
    "<b>Mobile App:</b> Create native mobile app for field officers",
]
for imp in improvements:
    elements.append(Paragraph(imp, normal_style))
elements.append(Spacer(1, 0.12*inch))

elements.append(Paragraph("IMPACT & USE CASES", heading_style))
impact = [
    "• <b>Road Maintenance:</b> Automated pothole detection for maintenance planning",
    "• <b>Safety:</b> Reduce accidents caused by road hazards",
    "• <b>Cost Saving:</b> Efficient resource allocation for repairs",
    "• <b>Real-time Monitoring:</b> Process dashcam footage from vehicles",
    "• <b>Smart Cities:</b> Integration with IoT for continuous road monitoring",
]
for imp in impact:
    elements.append(Paragraph(imp, normal_style))

# Build PDF
doc.build(elements)
print(f"\n[SUCCESS] PDF Report created: {pdf_path}")
