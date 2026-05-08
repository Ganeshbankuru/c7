#!/usr/bin/env python
"""
YOLOv8 Webcam Demo
This script runs YOLOv8 object detection on your webcam feed
"""

import cv2
from ultralytics import YOLO

def run_yolo_webcam():
    # Load the YOLOv8 model (using the default COCO model)
    model = YOLO('yolov8n.pt')
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    print("Starting YOLOv8 webcam demo...")
    print("Press 'q' to quit")
    
    while True:
        # Read frame from webcam
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
            
        # Run YOLO inference
        results = model(frame)
        
        # Visualize results
        annotated_frame = results[0].plot()
        
        # Display the frame
        cv2.imshow('YOLOv8 Inference', annotated_frame)
        
        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_yolo_webcam()