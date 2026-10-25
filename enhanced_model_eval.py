import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os

fig_dir = "chart_assets"
os.makedirs(fig_dir, exist_ok=True)

print("Creating ENHANCED model evaluation report...")

# ============================================================================
# Chart 1: MODEL & DATASET INFO with Metrics
# ============================================================================
print("Creating info panels...")

fig = plt.figure(figsize=(14, 7))
gs = fig.add_gridspec(2, 2, width_ratios=[1, 1], height_ratios=[1, 1], hspace=0.4, wspace=0.3)

# MODEL INFO (Top Left)
ax1 = fig.add_subplot(gs[0, 0])
ax1.axis('off')

model_text = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        MODEL INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Model Name:           YOLOv8n (best.pt)
Model Type:           Object Detection
Architecture:         Single-stage Detector
Framework:            PyTorch (Ultralytics)
Input Size:           640 × 640 pixels
Model Scale:          Nano (Lightweight)
Model Size:           6.2 MB
Training Device:      CPU
Inference Device:     CPU
Optimization:         FP32 (Full Precision)

Best Epoch:           Epoch 25
Model Status:         PRODUCTION READY
"""

ax1.text(0.05, 0.95, model_text, transform=ax1.transAxes,
        fontsize=9.5, verticalalignment='top', fontfamily='monospace',
        bbox=dict(boxstyle='round,pad=1.2', facecolor='#e3f2fd',
                 edgecolor='#0052CC', linewidth=2.5))

# DATASET INFO (Top Right)
ax2 = fig.add_subplot(gs[0, 1])
ax2.axis('off')

dataset_text = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
       DATASET INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Dataset Name:         Pothole - v1 (Raw)
Dataset Source:       Roboflow.ai
Export Date:          November 1, 2020

Total Images:         665
  Training:           465 (69.9%)
  Validation:         133 (20.0%)
  Test:               67 (10.1%)

Classes:              1 (Pothole Detection)
Annotation Format:    YOLO v4 PyTorch
Total Instances:      330 potholes
Pre-processing:       Auto-orientation
Augmentation:         RandAugment + Mosaic
"""

ax2.text(0.05, 0.95, dataset_text, transform=ax2.transAxes,
        fontsize=9.5, verticalalignment='top', fontfamily='monospace',
        bbox=dict(boxstyle='round,pad=1.2', facecolor='#f0fff0',
                 edgecolor='#28A745', linewidth=2.5))

# TRAINING INFO (Bottom Left)
ax3 = fig.add_subplot(gs[1, 0])
ax3.axis('off')

training_text = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      TRAINING INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Epochs Planned: 50
Epochs Completed:     28
Early Stopping:       YES (patience=3)

Best Epoch:           Epoch 25
Training Time:        1.105 hours
Stopped Reason:       No improvement
                      for 3 epochs

Batch Size:           2
Optimizer:            AdamW
Learning Rate:        0.002 (auto)
Momentum:             0.9
Weight Decay:         0.0005
IoU Threshold:        0.7
"""

ax3.text(0.05, 0.95, training_text, transform=ax3.transAxes,
        fontsize=9.5, verticalalignment='top', fontfamily='monospace',
        bbox=dict(boxstyle='round,pad=1.2', facecolor='#fff3e0',
                 edgecolor='#FFC107', linewidth=2.5))

# EPOCH PROGRESSION (Bottom Right)
ax4 = fig.add_subplot(gs[1, 1])
ax4.axis('off')

epoch_text = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    EPOCH PROGRESSION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Epoch 1:   P:39.8%  R:38.5%  mAP:33.8%
Epoch 5:   P:61.1%  R:46.2%  mAP:51.1%
Epoch 10:  P:70.9%  R:50.9%  mAP:58.9%
Epoch 15:  P:72.9%  R:58.8%  mAP:66.4%
Epoch 20:  P:71.4%  R:62.4%  mAP:68.2%
Epoch 25:  P:71.2%  R:64.5%  mAP:72.7% ★
Epoch 28:  P:69.9%  R:65.4%  mAP:68.7%

★ = BEST EPOCH (Highest mAP50-95: 43.2%)
"""

ax4.text(0.05, 0.95, epoch_text, transform=ax4.transAxes,
        fontsize=8.8, verticalalignment='top', fontfamily='monospace',
        bbox=dict(boxstyle='round,pad=1.2', facecolor='#fce4ec',
                 edgecolor='#DC3545', linewidth=2.5))

fig.suptitle('Complete Model, Dataset & Training Information',
            fontsize=16, fontweight='700', y=0.98)

plt.savefig(f'{fig_dir}/model_dataset_info.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("[OK] Model/Dataset info panels created")

# ============================================================================
# CONFUSION MATRIX - SQUARE with detailed annotations
# ============================================================================
print("Creating square confusion matrix...")

fig, ax = plt.subplots(figsize=(9, 9))

# Confusion matrix values
tp = 212
fp = 104
fn = 14
tn = 0

cm = np.array([[tp, fp], [fn, tn]])

# Create square confusion matrix heatmap
im = ax.imshow(cm, cmap='Blues', aspect='auto', alpha=0.85, vmin=0, vmax=max(tp, fp, fn))

# Set ticks and labels for SQUARE appearance
ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(['Predicted\nPositive', 'Predicted\nNegative'], fontsize=13, fontweight='700')
ax.set_yticklabels(['Actually\nPositive', 'Actually\nNegative'], fontsize=13, fontweight='700')

# Add text annotations with larger font
for i in range(2):
    for j in range(2):
        count = cm[i, j] if cm[i, j] >= 0 else 0
        percentage = (count / 330 * 100) if count > 0 else 0

        # Different colors for text based on cell
        text_color = "white" if count > 100 else "black"

        ax.text(j, i, f'{int(count)}\n({percentage:.1f}%)',
               ha="center", va="center", color=text_color,
               fontweight='700', fontsize=14)

# Add colorbar
cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('Count', fontsize=11, fontweight='600')

# Labels
ax.set_ylabel('Actual Label', fontsize=13, fontweight='700', labelpad=15)
ax.set_xlabel('Predicted Label', fontsize=13, fontweight='700', labelpad=15)
ax.set_title('Confusion Matrix - Pothole Detection (Epoch 25)',
            fontsize=15, fontweight='700', pad=20, color='#1a1a1a')

# Add grid for clarity
ax.set_xticks(np.arange(2)-.5, minor=True)
ax.set_yticks(np.arange(2)-.5, minor=True)
ax.grid(which="minor", color="gray", linestyle='-', linewidth=2)

# Add detailed metrics below
metrics_y = -0.35
ax.text(0.5, metrics_y,
       'Precision = TP/(TP+FP) = 212/316 = 67.1%  |  Recall = TP/(TP+FN) = 212/226 = 93.8%  |  Accuracy = (TP+TN)/(Total) = 64.2%',
       transform=ax.transAxes, ha='center', fontsize=10, fontweight='600',
       bbox=dict(boxstyle='round,pad=0.8', facecolor='#f5f5f5', edgecolor='#333', linewidth=1.5))

plt.tight_layout()
plt.subplots_adjust(bottom=0.15)
plt.savefig(f'{fig_dir}/confusion_matrix_square.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("[OK] Square confusion matrix created")

print("\n" + "="*70)
print("ENHANCED CHARTS CREATED!")
print("="*70)
print("[OK] Model & Dataset information panels")
print("[OK] Complete training epoch summary")
print("[OK] Square confusion matrix with metrics")
print("="*70)
