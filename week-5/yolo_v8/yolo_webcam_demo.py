#!/usr/bin/env python
import cv2
from ultralytics import YOLO
from utils.draw_boxes import draw_boxes

def main():
    cap = cv2.VideoCapture(0)
    print("Starting YOLOv8 webcam demo...")
    print("Press 'q' to quit")

    # Load YOLOv8 model
    model = YOLO('yolov8_weights/yolov8n.pt')

    while True:
        ret, frame = cap.read()  # Read frame from webcam
        if not ret:
            print("Failed to grab frame")
            break
        # Run YOLO inference
        results = model(frame)  # Run YOLO inference
        boxes = results[0].boxes.xyxy.cpu().numpy()
        scores = results[0].boxes.conf.cpu().numpy()
        class_ids = results[0].boxes.cls.cpu().numpy().astype(int)
        class_names = model.names
        frame = draw_boxes(frame, boxes, scores, class_ids, class_names)
        # Display the frame
        cv2.imshow('YOLOv8 Webcam', frame)
        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()