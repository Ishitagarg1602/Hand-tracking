from ultralytics import YOLO

if __name__ == '__main__':
    print("Initializing training...")
    # Load a pretrained model (recommended for training)
    model = YOLO("yolov8n.pt")

    # Train the model
    print("Starting training on your data.yaml...")
    results = model.train(data="data.yaml", epochs=50, imgsz=640)
    
    print("\nTraining complete! Your trained model is normally saved to runs/detect/train/weights/best.pt")
