# YOLOv8 Implementation Guide

This guide explains how to implement YOLOv8 for object detection with webcam input and how to create a custom dataset using Roboflow.

## Task 1: Run YOLOv8 on Webcam

### Installation Requirements

To run YOLOv8 with webcam support, you'll need:

```bash
pip install ultralytics opencv-python
```

### Running the Demo

1. Save the provided Python script (`yolo_webcam_demo.py`)
2. Execute it:
```bash
python yolo_webcam_demo.py
```

3. The camera feed will appear in a window showing real-time object detection
4. Press 'q' to quit the application

### How It Works

- Loads the pretrained YOLOv8 nano model (`yolov8n.pt`)
- Captures video from your default webcam (index 0)
- Runs real-time object detection on each frame
- Displays the annotated frames with bounding boxes and labels

## Task 2: Create Custom Dataset via Roboflow (Optional)

### Steps to Create Custom Dataset:

1. **Sign up for Roboflow** (free account available at [roboflow.com](https://roboflow.com))

2. **Create a New Project**:
   - Navigate to "Create new project"
   - Choose "Object Detection" task
   - Select "YOLOv8" as export format

3. **Upload Images**:
   - Add your training images to the project
   - Label your objects using the annotation tools

4. **Train Your Model**:
   - Use Roboflow's training interface or export dataset for local training

5. **Export Model**:
   - Export your trained model in YOLOv8 format to use in your Python code

### Using Your Custom Dataset in Code

After creating your custom model, replace the model loading line in the demo script:

```python
# Replace this line:
model = YOLO('yolov8n.pt')

# With your custom model:
model = YOLO('path/to/your/custom/model.pt')
```

### Important Notes

- YOLOv8 pre-trained models recognize 80 common classes by default
- Custom datasets allow you to train on your specific objects
- Roboflow automates dataset preparation and export in various formats
- For best results, your custom dataset should contain several hundred labeled images