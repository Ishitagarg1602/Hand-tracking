# Gesture Controlled Computer System ✋💻

This project allows you to control your computer using your webcam and customized hand gestures. It uses **OpenCV** for video capture, **YOLOv8** for gesture recognition, and **PyAutoGUI** / **screen_brightness_control** to execute computer actions (volume control, taking screenshots, scrolling, and brightness control).

## Supported Gestures & Actions

- 👍 **Thumbs Up**: Increase Volume
- ✋ **Open Palm**: Take Screenshot (Saves as `screenshot_<timestamp>.png` in the directory)
- ✊ **Fist**: Scroll Down (Smooth downward scrolling)
- 👉 **Swipe Right**: Increase Screen Brightness
- 👈 **Swipe Left**: Decrease Screen Brightness

*Note*: Actions have specific cooldown times implemented to prevent the program from spamming operations continuously when a gesture is held on screen. The system provides visual feedback indicating "READY" or "ACTION ACTIVE" (cooldown) on the camera feed.

## Prerequisites

1. Install Python 3.8+ 
2. Install the necessary requirements:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: ensure you have `screen-brightness-control` installed as well. You can manually install it via `pip install screen-brightness-control`)*

## How to use (Complete Guide)

Since this project requires a customized YOLOv8 model for detecting your hands, follow these steps to collect data, train your model, and run the system.

### 1. Data Collection
We need to capture photos of your hand performing the 5 gestures.
1. Run the data collection script:
   ```bash
   python data_collection.py
   ```
2. Press **'n'** to select the gesture you want to capture at the top left corner of the feed.
3. Press **'s'** to save an image. Make sure to move your hand around (closer, further, different angles). Take ~30 to 50 images per gesture.
4. Press **'q'** to quit.
   
This will create a `dataset/images/` folder containing all your pictures, sorted by gesture class.

### 2. Labeling the Data
1. You can use a tool like [MakeSense.ai](https://www.makesense.ai/) or [LabelImg](https://github.com/HumanSignal/labelImg) to label your images locally, or upload them to [Roboflow.com](https://roboflow.com).
2. Draw bounding boxes around your hand in each image and label them exactly with these class names:
   - `thumbs_up`
   - `open_palm`
   - `fist`
   - `swipe_right`
   - `swipe_left`
3. Export your labels in the **YOLO format** matching the dataset and place the `.txt` label files in a new `dataset/labels/` directory. 

### 3. Splitting Data and Training the YOLOv8 Model
We have provided scripts to help you organize data and train effortlessly.
1. Run the script to split your data randomly into 80% training and 20% validation sets:
   ```bash
   python split_data.py
   ```
   *(Ensure you have your labels in `dataset/labels` and your images in `dataset/images` prior to running this script.)*

2. Create or verify your `data.yaml` config file. It should point to the generated `dataset/images/train/` and `dataset/images/val/` paths, and list the 5 string classes under the `names` configuration.

3. Run the training script automatically to download `yolov8n.pt` and train on your local dataset:
   ```bash
   python train.py
   ```

4. After training finishes, your newly trained model weights will be saved in `runs/detect/train/weights/best.pt`.
5. **Ensure the `best.pt` file is copied into this project's root main directory!**

### 4. Running the System
Now the fun part! You can run your system:
```bash
python main.py
```
Stand in front of the camera and perform the gestures! An on-screen UI will display the gesture detection confidence and bounding boxes. Perform any of the 5 trained gestures to execute the mapped commands. Press **'q'** to exit the application.
