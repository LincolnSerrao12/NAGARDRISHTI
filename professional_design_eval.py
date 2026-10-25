import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

fig_dir = "chart_assets"
os.makedirs(fig_dir, exist_ok=True)

print("Creating PROFESSIONALLY DESIGNED charts with proper spacing...")

# PROFESSIONAL DESIGN SYSTEM
# ============================================================================
# Spacing Scale (8px baseline)
SPACING_XS = 0.25  # 8px
SPACING_SM = 0.5   # 16px
SPACING_MD = 0.75  # 24px
SPACING_LG = 1.0   # 32px
SPACING_XL = 1.5   # 48px

# Padding Scale
PADDING_SM = 0.15  # 12px
PADDING_MD = 0.25  # 20px
PADDING_LG = 0.35  # 28px

# Colors
COLOR_PRIMARY = '#0052CC'
COLOR_SUCCESS = '#28A745'
COLOR_INFO = '#17A2B8'
COLOR_WARNING = '#FFC107'
COLOR_DANGER = '#DC3545'
COLOR_NEUTRAL_LIGHT = '#F8F9FA'
COLOR_NEUTRAL_DARK = '#343A40'
COLOR_TEXT = '#1A1A1A'
COLOR_TEXT_SECONDARY = '#666666'

# ============================================================================
# PROFESSIONAL INFO PANELS WITH PROPER SPACING
# ============================================================================
print("Creating professional info panels...")

fig = plt.figure(figsize=(14, 9))
# Use GridSpec for precise control
gs = fig.add_gridspec(2, 2, width_ratios=[1, 1], height_ratios=[1, 1],
                     hspace=0.35, wspace=0.3,  # Professional spacing
                     left=0.08, right=0.95, top=0.93, bottom=0.06)

# Color scheme for each panel
panel_configs = [
    {'title': 'MODEL INFORMATION', 'color': '#E3F2FD', 'border': COLOR_PRIMARY, 'text_color': COLOR_TEXT},
    {'title': 'DATASET INFORMATION', 'color': '#F1F8E9', 'border': COLOR_SUCCESS, 'text_color': COLOR_TEXT},
    {'title': 'TRAINING INFORMATION', 'color': '#FFF3E0', 'border': COLOR_WARNING, 'text_color': COLOR_TEXT},
    {'title': 'EPOCH PROGRESSION', 'color': '#FCE4EC', 'border': COLOR_DANGER, 'text_color': COLOR_TEXT},
]

model_info = """Model Name:           YOLOv8n (best.pt)
Model Type:           Object Detection
Architecture:         Single-stage Detector
Framework:            PyTorch (Ultralytics)
Input Size:           640 × 640 pixels
Model Scale:          Nano (Lightweight)
Model Size:           6.2 MB
Training Device:      CPU
Inference Device:     CPU
Optimization:         FP32
Best Epoch:           Epoch 25
Model Status:         PRODUCTION READY"""

dataset_info = """Dataset Name:         Pothole - v1 (Raw)
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
Augmentation:         RandAugment + Mosaic"""

training_info = """Total Epochs Planned: 50
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
IoU Threshold:        0.7"""

epoch_info = """Epoch  1: P:39.8%  R:38.5%  mAP:33.8%
Epoch  5: P:61.1%  R:46.2%  mAP:51.1%
Epoch 10: P:70.9%  R:50.9%  mAP:58.9%
Epoch 15: P:72.9%  R:58.8%  mAP:66.4%
Epoch 20: P:71.4%  R:62.4%  mAP:68.2%
Epoch 25: P:71.2%  R:64.5%  mAP:72.7% ★
Epoch 28: P:69.9%  R:65.4%  mAP:68.7%

★ = BEST EPOCH
(Highest mAP50-95: 43.2%)"""

info_data = [
    (0, 0, model_info, panel_configs[0]),
    (0, 1, dataset_info, panel_configs[1]),
    (1, 0, training_info, panel_configs[2]),
    (1, 1, epoch_info, panel_configs[3]),
]

for row, col, text_content, config in info_data:
    ax = fig.add_subplot(gs[row, col])
    ax.axis('off')

    # Professional box styling with proper padding
    box = mpatches.FancyBboxPatch(
        (0.02, 0.02), 0.96, 0.96,
        boxstyle="round,pad=0.025",
        transform=ax.transAxes,
        edgecolor=config['border'],
        facecolor=config['color'],
        linewidth=3,
        zorder=0
    )
    ax.add_patch(box)

    # Title with proper spacing
    ax.text(0.5, 0.97, config['title'],
           transform=ax.transAxes,
           fontsize=13, fontweight='700',
           ha='center', va='top',
           color=config['border'],
           bbox=dict(boxstyle='round,pad=0.4',
                    facecolor='white',
                    edgecolor=config['border'],
                    linewidth=2))

    # Content with professional spacing
    ax.text(0.08, 0.87, text_content,
           transform=ax.transAxes,
           fontsize=9.2, verticalalignment='top',
           fontfamily='monospace',
           color=COLOR_TEXT,
           linespacing=1.8,
           bbox=dict(boxstyle='round,pad=0.8',
                    facecolor='white',
                    edgecolor='#DDDDDD',
                    linewidth=1,
                    alpha=0.95))

# Main title with proper spacing
fig.text(0.5, 0.98, 'Complete Model, Dataset & Training Information',
        fontsize=16, fontweight='700', ha='center',
        color=COLOR_TEXT)

plt.savefig(f'{fig_dir}/model_dataset_info_pro.png', dpi=300, bbox_inches='tight',
           facecolor='white', edgecolor='none', pad_inches=0.2)
plt.close()
print("[OK] Professional info panels with proper spacing")

# ============================================================================
# PROFESSIONAL SQUARE CONFUSION MATRIX
# ============================================================================
print("Creating professional confusion matrix...")

fig, ax = plt.subplots(figsize=(10, 10))

# Data
tp, fp, fn, tn = 212, 104, 14, 0
cm = np.array([[tp, fp], [fn, tn]])

# Professional heatmap with spacing
im = ax.imshow(cm, cmap='Blues', aspect='auto', alpha=0.85, vmin=0, vmax=max(tp, fp, fn))

# Professional axis styling
ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(['Predicted\nPositive', 'Predicted\nNegative'],
                   fontsize=13, fontweight='700', color=COLOR_TEXT)
ax.set_yticklabels(['Actually\nPositive', 'Actually\nNegative'],
                   fontsize=13, fontweight='700', color=COLOR_TEXT)

# Professional grid
for spine in ax.spines.values():
    spine.set_edgecolor(COLOR_TEXT)
    spine.set_linewidth(2)

# Cell annotations with professional spacing
for i in range(2):
    for j in range(2):
        count = cm[i, j] if cm[i, j] >= 0 else 0
        percentage = (count / 330 * 100) if count > 0 else 0
        text_color = "white" if count > 100 else COLOR_TEXT

        # Professional text styling
        ax.text(j, i, f'{int(count)}\n({percentage:.1f}%)',
               ha="center", va="center",
               color=text_color, fontweight='700', fontsize=15,
               bbox=dict(boxstyle='round,pad=0.5',
                        facecolor='none', edgecolor='none'))

# Professional axis labels
ax.set_ylabel('Actual Label', fontsize=14, fontweight='700',
             color=COLOR_TEXT, labelpad=20)
ax.set_xlabel('Predicted Label', fontsize=14, fontweight='700',
             color=COLOR_TEXT, labelpad=20)

# Professional title with spacing
ax.set_title('Confusion Matrix - Pothole Detection (Epoch 25)',
            fontsize=16, fontweight='700', pad=25, color=COLOR_TEXT)

# Colorbar with professional styling
cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.08)
cbar.set_label('Count', fontsize=12, fontweight='700', labelpad=15)
cbar.ax.tick_params(labelsize=10)

# Professional metrics box below with proper spacing
metrics_text = ('Precision = 212/316 = 67.1%  |  Recall = 212/226 = 93.8%  |  '
               'Accuracy = 212/330 = 64.2%')
fig.text(0.5, 0.06, metrics_text,
        ha='center', fontsize=11, fontweight='600',
        bbox=dict(boxstyle='round,pad=0.8',
                 facecolor=COLOR_NEUTRAL_LIGHT,
                 edgecolor=COLOR_TEXT,
                 linewidth=2))

plt.tight_layout()
plt.subplots_adjust(bottom=0.15)
plt.savefig(f'{fig_dir}/confusion_matrix_pro.png', dpi=300, bbox_inches='tight',
           facecolor='white', pad_inches=0.2)
plt.close()
print("[OK] Professional confusion matrix with proper spacing")

print("\n" + "="*70)
print("PROFESSIONAL DESIGN COMPLETE!")
print("="*70)
print("[OK] Proper spacing & padding throughout")
print("[OK] Professional visual hierarchy")
print("[OK] Clean, minimal aesthetic")
print("[OK] Readable typography with proper line spacing")
print("[OK] Professional color system")
print("="*70)
