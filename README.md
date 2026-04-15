# Gesture Controlled Computer System ✋💻

This project allows you to control your computer using your webcam and customized hand gestures.
It uses **OpenCV** for video capture, **YOLOv8** for gesture recognition, and **PyAutoGUI** to execute computer actions (volume up, next slide, play/pause video).

## Prerequisites

1. Install Python 3.8+ 
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

## How to use (Complete Guide)

Since this uses a custom YOLOv8 model for your hands, you need to follow these steps to build your model.

### 1. Data Collection
We need to capture photos of your hand performing the 5 gestures (Thumbs Up, Open Palm, Fist, Swipe Right, Swipe Left).
1. Run the data collection script:
   ```bash
   python data_collection.py
   ```
2. Press **'s'** to save an image. Make sure to move your hand around (closer, further, different angles). Take ~30 to 50 images per gesture.
3. Press **'n'** to switch to the next gesture.
4. Press **'q'** to quit.
   
This will create a `dataset/images` folder containing all your pictures.

### 2. Labeling the Data
1. Go to [Roboflow.com](https://roboflow.com) (or use LabelImg locally if you prefer).
2. Create a new *Object Detection* project.
3. Upload all the images from `dataset/images`.
4. Draw bounding boxes around your hand in each image and assign the correct class name (`thumbs_up`, `open_palm`, `fist`, `swipe_right`, `swipe_left`).
5. Generate a dataset and select export format: **YOLOv8**.

### 3. Training the YOLOv8 Model
1. Once you download the dataset from Roboflow, open the Terminal/Command Prompt in your dataset directory.
2. Run the Ultralytics training command. (This will download `yolov8n.pt` and train on your `data.yaml`):
   ```bash
   yolo detect train data=data.yaml model=yolov8n.pt epochs=50 imgsz=640
   ```
3. After training finishes, your model weights will be saved in `runs/detect/train/weights/best.pt`.
4. **Copy the `best.pt` file into this project's main directory.**

### 4. Running the System
Now the fun part! You can run your system:
```bash
python main.py
```
Stand in front of the camera and perform the gestures:
- 👍 **Thumbs Up**: Increases volume
- ✋ **Open Palm**: Take Screenshot  
- ✊ **Fist**:  scrolls 
- 👉 **Swipe Right**:  Brightness increase 
- 👈 **Swipe Left**:Brightness decrease    

---
*Note: A 2-second cooldown is implemented to prevent the program from spamming keystrokes when a gesture is held on screen.*