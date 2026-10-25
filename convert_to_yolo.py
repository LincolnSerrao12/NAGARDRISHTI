"""
Convert Pascal VOC annotations to YOLO format
"""

import os
from PIL import Image
from pathlib import Path

def convert_voc_to_yolo(voc_format_line, image_width, image_height):
    """
    Convert Pascal VOC coordinates to YOLO format
    VOC: x1,y1,x2,y2 (pixel coordinates)
    YOLO: center_x,center_y,width,height (normalized 0-1)
    """
    yolo_annotations = []
    parts = voc_format_line.split()

    # Skip first part (filename)
    coords = parts[1:]

    for coord_str in coords:
        x1, y1, x2, y2, class_id = map(float, coord_str.split(','))

        # Calculate center and width/height
        center_x = (x1 + x2) / 2 / image_width
        center_y = (y1 + y2) / 2 / image_height
        width = (x2 - x1) / image_width
        height = (y2 - y1) / image_height

        # Clamp values to [0, 1]
        center_x = max(0, min(1, center_x))
        center_y = max(0, min(1, center_y))
        width = max(0, min(1, width))
        height = max(0, min(1, height))

        yolo_annotations.append(f"{int(class_id)} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}")

    return yolo_annotations

def convert_dataset(dataset_path):
    """Convert entire dataset to YOLO format"""

    for split in ['train', 'valid', 'test']:
        split_path = os.path.join(dataset_path, split)
        annotations_file = os.path.join(split_path, '_annotations.txt')

        if not os.path.exists(annotations_file):
            print(f"⚠️  {split}/_annotations.txt not found, skipping")
            continue

        print(f"\n📝 Converting {split} annotations...")

        with open(annotations_file, 'r') as f:
            lines = f.readlines()

        success = 0
        for line in lines:
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            image_filename = parts[0]
            image_path = os.path.join(split_path, image_filename)

            # Get image dimensions
            try:
                img = Image.open(image_path)
                width, height = img.size
            except Exception as e:
                print(f"  ⚠️  Could not read {image_filename}: {e}")
                continue

            # Convert annotations
            yolo_annots = convert_voc_to_yolo(line, width, height)

            # Write YOLO format label file
            label_filename = image_filename.rsplit('.', 1)[0] + '.txt'
            label_path = os.path.join(split_path, label_filename)

            with open(label_path, 'w') as f:
                for annot in yolo_annots:
                    f.write(annot + '\n')

            success += 1

        print(f"  ✅ Converted {success}/{len(lines)} annotations for {split}")

if __name__ == "__main__":
    dataset_path = "Pothole.v1-raw.yolov4pytorch"

    print("=" * 70)
    print("Converting Pascal VOC annotations to YOLO format")
    print("=" * 70)

    convert_dataset(dataset_path)

    print("\n" + "=" * 70)
    print("✅ Conversion complete!")
    print("=" * 70)
    print("\nYou can now run: python train_yolo.py")
