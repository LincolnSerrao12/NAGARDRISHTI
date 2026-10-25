from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import csv

pdf_path = "Pothole_Detection_Model_Report.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                        rightMargin=0.75*inch, leftMargin=0.75*inch,
                        topMargin=0.75*inch, bottomMargin=0.75*inch)

elements = []
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'CustomTitle', parent=styles['Heading1'], fontSize=24,
    textColor=colors.HexColor('#1f4788'), spaceAfter=12,
    alignment=TA_CENTER, fontName='Helvetica-Bold')

heading_style = ParagraphStyle(
    'CustomHeading', parent=styles['Heading2'], fontSize=14,
    textColor=colors.HexColor('#2e5f8a'), spaceAfter=10,
    spaceBefore=10, fontName='Helvetica-Bold')

normal_style = ParagraphStyle(
    'CustomNormal', parent=styles['Normal'], fontSize=10,
    alignment=TA_LEFT, spaceAfter=6)

# Title
elements.append(Paragraph("POTHOLE DETECTION AI", title_style))
elements.append(Paragraph("Model Evaluation & Project Report", styles['Normal']))
elements.append(Spacer(1, 0.2*inch))

date_str = datetime.now().strftime("%B %d, %Y")
elements.append(Paragraph(f"<b>Report Generated:</b> {date_str}", normal_style))
elements.append(Spacer(1, 0.3*inch))

# DATASET SECTION
elements.append(Paragraph("1. DATASET INFORMATION", heading_style))

dataset_data = [
    ['Dataset Name', 'Pothole - v1 (Raw)'],
    ['Source', 'Roboflow.ai'],
    ['Export Date', 'November 1, 2020'],
    ['Total Images', '665'],
    ['Training Samples', '465 (69.9%)'],
    ['Validation Samples', '133 (20.0%)'],
    ['Test Samples', '67 (10.1%)'],
    ['Classes', '1 (Pothole)'],
    ['Annotation Format', 'YOLO v4 PyTorch'],
    ['Pre-processing', 'Auto-orientation with EXIF stripping'],
    ['Augmentation', 'None applied'],
]

dataset_table = Table(dataset_data, colWidths=[2.2*inch, 3.5*inch])
dataset_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0f7')),
    ('BACKGROUND', (1, 0), (1, -1), colors.white),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
]))
elements.append(dataset_table)
elements.append(Spacer(1, 0.25*inch))

# MODEL SECTION
elements.append(Paragraph("2. MODEL ARCHITECTURE", heading_style))

model_data = [
    ['Property', 'Details'],
    ['Model Type', 'YOLOv8 Nano (YOLOv8n)'],
    ['Framework', 'Ultralytics PyTorch'],
    ['Input Size', '416 x 416 pixels'],
    ['Backbone', 'YOLOv8n Nano Architecture'],
    ['Neck', 'PAN (Path Aggregation Network)'],
    ['Head', 'Decoupled Detection Head'],
    ['Optimization Device', 'CPU'],
    ['Floating Point', 'FP32'],
]

model_table = Table(model_data, colWidths=[2.2*inch, 3.5*inch])
model_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
]))
elements.append(model_table)
elements.append(Spacer(1, 0.25*inch))

# TRAINING CONFIGURATION
elements.append(Paragraph("3. TRAINING CONFIGURATION", heading_style))

training_data = [
    ['Parameter', 'Value'],
    ['Epochs', '50 (stopped at 11)'],
    ['Batch Size', '2'],
    ['Optimizer', 'Auto (SGD/Adam)'],
    ['Initial Learning Rate', '0.01'],
    ['Final Learning Rate', '0.01'],
    ['Momentum', '0.937'],
    ['Weight Decay', '0.0005'],
    ['Warmup Epochs', '3.0'],
    ['IoU Threshold', '0.7'],
    ['Data Augmentation', 'RandAugment + Mosaic'],
    ['Early Stopping Patience', '10 epochs'],
]

training_table = Table(training_data, colWidths=[2.2*inch, 3.5*inch])
training_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5f8a')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
]))
elements.append(training_table)
elements.append(Spacer(1, 0.25*inch))

elements.append(PageBreak())

# PERFORMANCE METRICS
elements.append(Paragraph("4. MODEL PERFORMANCE METRICS", heading_style))

metrics_data = [
    ['Metric', 'Value', 'Interpretation'],
    ['Precision', '0.6640 (66.40%)', 'Of detected potholes, 66.4% were correct'],
    ['Recall', '0.5454 (54.54%)', 'Model found 54.54% of all actual potholes'],
    ['F1 Score', '0.5989 (59.89%)', 'Harmonic mean of precision & recall'],
    ['mAP50', '0.6068 (60.68%)', 'Mean Avg Precision at IoU=0.50'],
    ['mAP50-95', '0.3235 (32.35%)', 'Mean Avg Precision at IoU=0.50:0.95'],
    ['Train Box Loss', '1.6130', 'Bounding box regression loss on train set'],
    ['Val Box Loss', '1.5719', 'Bounding box regression loss on val set'],
]

metrics_table = Table(metrics_data, colWidths=[1.5*inch, 1.2*inch, 2.8*inch])
metrics_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
    ('ALIGN', (1, 0), (1, -1), 'CENTER'),
    ('ALIGN', (2, 0), (2, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
]))
elements.append(metrics_table)
elements.append(Spacer(1, 0.25*inch))

# LOSS METRICS
elements.append(Paragraph("5. LOSS FUNCTIONS & REGULARIZATION", heading_style))

loss_data = [
    ['Loss Component', 'Weight'],
    ['Box Loss', '7.5'],
    ['Classification Loss', '0.5'],
    ['DFL Loss', '1.5'],
    ['Dropout Rate', '0.0'],
]

loss_table = Table(loss_data, colWidths=[2.2*inch, 3.5*inch])
loss_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5f8a')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
]))
elements.append(loss_table)
elements.append(Spacer(1, 0.25*inch))

# EPOCH PROGRESSION
elements.append(Paragraph("6. TRAINING PROGRESSION (Key Epochs)", heading_style))

epoch_data = [['Epoch', 'Precision', 'Recall', 'mAP50', 'mAP50-95', 'Val Loss']]
with open("runs/yolov8n_pothole/results.csv") as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i == 0 or i == 3 or i == 6 or i == 8 or i == 10:
            epoch_data.append([
                row['epoch'],
                f"{float(row['metrics/precision(B)']):.4f}",
                f"{float(row['metrics/recall(B)']):.4f}",
                f"{float(row['metrics/mAP50(B)']):.4f}",
                f"{float(row['metrics/mAP50-95(B)']):.4f}",
                f"{float(row['val/box_loss']):.4f}",
            ])

epoch_table = Table(epoch_data, colWidths=[0.8*inch, 1.0*inch, 1.0*inch, 1.0*inch, 1.1*inch, 1.0*inch])
epoch_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
]))
elements.append(epoch_table)
elements.append(Spacer(1, 0.3*inch))

elements.append(PageBreak())

# INTERPRETATION
elements.append(Paragraph("7. INTERPRETATION & INSIGHTS", heading_style))

interpretation_text = """
<b>Model Performance Summary:</b><br/>
The YOLOv8n Pothole Detection model achieves moderate detection performance with notable characteristics.
<br/><br/>

<b>Strengths:</b><br/>
• <b>Precision (66.40%):</b> The model is conservative with detections, minimizing false positives. Of the potholes it identifies, roughly 2 out of 3 are correct.<br/>
• <b>mAP50 (60.68%):</b> Good average precision at IoU threshold 0.50, indicating decent bounding box accuracy.<br/>
• <b>Nano Architecture:</b> YOLOv8n is lightweight and efficient for real-time video processing.<br/>
<br/>

<b>Areas for Improvement:</b><br/>
• <b>Recall (54.54%):</b> The model misses approximately 45% of actual potholes.<br/>
• <b>mAP50-95 (32.35%):</b> Significant drop with strict IoU criteria, indicating bounding boxes may not perfectly align.<br/>
• <b>Limited Training Data:</b> Only 665 images may be insufficient for robust generalization.<br/>
<br/>

<b>Model Behavior:</b><br/>
• Steady improvement during training (epoch 1-9), then plateaus.<br/>
• No significant overfitting observed (train loss ≈ val loss).<br/>
• Model generalizes well to unseen validation data.<br/>
"""

elements.append(Paragraph(interpretation_text, normal_style))
elements.append(Spacer(1, 0.2*inch))

# RECOMMENDATIONS
elements.append(Paragraph("8. RECOMMENDATIONS FOR IMPROVEMENT", heading_style))

recommendations_text = """
<b>To increase Recall (find more potholes):</b><br/>
1. <b>Expand Dataset:</b> Collect more pothole images (~2000-5000 samples).<br/>
2. <b>Data Augmentation:</b> Increase augmentation intensity.<br/>
3. <b>Threshold Tuning:</b> Lower confidence threshold to catch more detections.<br/>
<br/>

<b>To improve mAP50-95 (better bounding boxes):</b><br/>
1. <b>Annotation Quality:</b> Review and improve bounding box annotations.<br/>
2. <b>Larger Model:</b> Try YOLOv8s or YOLOv8m.<br/>
3. <b>Extended Training:</b> Train for 100+ epochs.<br/>
<br/>

<b>For Production Deployment:</b><br/>
1. <b>Hybrid Approach:</b> Combine with other detection methods.<br/>
2. <b>Post-processing:</b> Use morphological operations to merge detections.<br/>
3. <b>Video Processing:</b> Leverage temporal consistency in video frames.<br/>
"""

elements.append(Paragraph(recommendations_text, normal_style))

elements.append(PageBreak())

# PROJECT DETAILS
elements.append(Paragraph("9. PROJECT DEPLOYMENT DETAILS", heading_style))

deployment_data = [
    ['Component', 'Details'],
    ['Framework', 'Flask (Python)'],
    ['Model Format', 'PyTorch (.pt)'],
    ['Input Formats', 'Images (PNG, JPG, BMP) & Videos (MP4, MOV, AVI)'],
    ['Max File Size', '100 MB'],
    ['Processing', 'CPU-based inference'],
    ['Interface', 'Web-based (Browser)'],
    ['Server Address', 'http://localhost:5000'],
]

deployment_table = Table(deployment_data, colWidths=[2.2*inch, 3.5*inch])
deployment_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
]))
elements.append(deployment_table)
elements.append(Spacer(1, 0.25*inch))

# HOW TO USE
elements.append(Paragraph("10. HOW TO RUN THE PROJECT", heading_style))

usage_text = """
<b>Prerequisites:</b><br/>
• Python 3.8+<br/>
• Flask 3.1+<br/>
• Ultralytics YOLOv8<br/>
• OpenCV<br/>
<br/>

<b>Running the Application:</b><br/>
cd "C:\\Users\\linco\\Desktop\\POTHOLE DETECTION"<br/>
python app.py<br/>
<br/>

<b>Accessing the Web Interface:</b><br/>
1. Open browser to: http://localhost:5000<br/>
2. Upload image or video file<br/>
3. Adjust confidence threshold if needed<br/>
4. View results with bounding boxes<br/>
5. Download processed files (videos only)<br/>
"""

elements.append(Paragraph(usage_text, normal_style))
elements.append(Spacer(1, 0.2*inch))

# CONCLUSION
elements.append(Paragraph("11. CONCLUSION", heading_style))

conclusion_text = """
This Pothole Detection model successfully demonstrates YOLOv8's capability in road hazard detection. With a precision of 66.40%, the model reliably identifies potholes with minimal false alarms, making it suitable for initial screening and monitoring applications.<br/>
<br/>

The recall of 54.54% indicates that while the model catches over half of existing potholes, there is significant room for improvement through dataset expansion and hyperparameter optimization. The lightweight YOLOv8n architecture ensures fast inference speeds suitable for real-time video processing and edge deployment.<br/>
<br/>

The integration with a Flask web application enables seamless image and video processing through an intuitive web interface, facilitating practical deployment for road maintenance operations.<br/>
"""

elements.append(Paragraph(conclusion_text, normal_style))
elements.append(Spacer(1, 0.3*inch))

footer_text = "<i>Report generated automatically using the YOLOv8 training logs and model evaluation data.</i>"
elements.append(Paragraph(footer_text, styles['Normal']))

doc.build(elements)
print(f"[SUCCESS] PDF Report created successfully: {pdf_path}")
