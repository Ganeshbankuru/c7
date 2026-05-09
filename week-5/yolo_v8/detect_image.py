import argparse
import cv2
from ultralytics import YOLO
import os

# Parse arguments
parser = argparse.ArgumentParser(description='YOLOv8 Image Detection')
parser.add_argument('--source', type=str, required=True, help='Path to input image')
parser.add_argument('--weights', type=str, default='yolov8_weights/yolov8n.pt', help='Path to YOLOv8 weights')
parser.add_argument('--output', type=str, default='output/detected_sample.jpg', help='Path to save output image')
args = parser.parse_args()

# Load model
model = YOLO(args.weights)

# Read image
image = cv2.imread(args.source)
if image is None:
    raise FileNotFoundError(f"Image not found: {args.source}")

# Run detection
results = model(image)
boxes = results[0].boxes.xyxy.cpu().numpy()
scores = results[0].boxes.conf.cpu().numpy()
class_ids = results[0].boxes.cls.cpu().numpy().astype(int)
class_names = model.names

# Draw boxes
from utils.draw_boxes import draw_boxes
image = draw_boxes(image, boxes, scores, class_ids, class_names)

# Save result
os.makedirs(os.path.dirname(args.output), exist_ok=True)
cv2.imwrite(args.output, image)
print(f"Saved: {args.output}")
