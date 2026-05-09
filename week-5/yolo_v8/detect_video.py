import argparse
import cv2
from ultralytics import YOLO
import os

parser = argparse.ArgumentParser(description='YOLOv8 Video Detection')
parser.add_argument('--source', type=str, required=True, help='Path to input video')
parser.add_argument('--weights', type=str, default='yolov8_weights/yolov8n.pt', help='Path to YOLOv8 weights')
parser.add_argument('--output', type=str, default='output/detected_sample.mp4', help='Path to save output video')
args = parser.parse_args()

model = YOLO(args.weights)

cap = cv2.VideoCapture(args.source)
if not cap.isOpened():
    raise FileNotFoundError(f"Video not found: {args.source}")

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = None

from utils.draw_boxes import draw_boxes

while True:
    ret, frame = cap.read()
    if not ret:
        break
    results = model(frame)
    boxes = results[0].boxes.xyxy.cpu().numpy()
    scores = results[0].boxes.conf.cpu().numpy()
    class_ids = results[0].boxes.cls.cpu().numpy().astype(int)
    class_names = model.names
    frame = draw_boxes(frame, boxes, scores, class_ids, class_names)
    if out is None:
        h, w = frame.shape[:2]
        out = cv2.VideoWriter(args.output, fourcc, cap.get(cv2.CAP_PROP_FPS), (w, h))
    out.write(frame)

cap.release()
if out:
    out.release()
print(f"Saved: {args.output}")
