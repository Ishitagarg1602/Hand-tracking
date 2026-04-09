import cv2
import pyautogui
import time
from ultralytics import YOLO

# Configuration
MODEL_PATH = "best.pt" # Replace with your trained YOLOv8 model file
CONFIDENCE_THRESHOLD = 0.70 # Minimum confidence score to execute action

# Time cooldown between actions (in seconds) to prevent command spamming!
COOLDOWN_TIME = 2.0 
last_action_time = 0

print("Initializing YOLO Model...")
try:
    model = YOLO(MODEL_PATH)
    print("Model loaded successfully!")
except Exception as e:
    print(f"\n[ERROR] Failed to load model '{MODEL_PATH}'.")
    print("Please make sure you have trained your model and placed 'best.pt' in the current directory.")
    print("Error details:", str(e))
    exit()

def execute_command(gesture_name):
    """
    Map the gesture to the corresponding computer command using PyAutoGUI.
    """
    global last_action_time
    
    current_time = time.time()
    if current_time - last_action_time < COOLDOWN_TIME:
        # Avoid spamming actions
        return

    print(f"Executing action for gesture: {gesture_name}")
    
    if gesture_name == 'thumbs_up':
        # Increase Volume
        pyautogui.press('volumeup')
    
    elif gesture_name == 'open_palm':
        # Pause Video
        pyautogui.press('space')
    
    elif gesture_name == 'fist':
        # Play Video 
        pyautogui.press('space')
        
    elif gesture_name == 'swipe_right':
        # Next Slide
        pyautogui.press('right')
    
    elif gesture_name == 'swipe_left':
        # Previous Slide
        pyautogui.press('left')
        
    # Update time of last action
    last_action_time = current_time

# Initialize Webcam
cap = cv2.VideoCapture(0)

print("\nStarting System... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    # Mirror the frame so it behaves like a mirror
    frame = cv2.flip(frame, 1)
    
    # Run YOLO object detection/classification on the frame
    results = model(frame, verbose=False)
    
    # If using an Object Detection model (predicts bounding boxes + classes)
    detected_gesture = None
    highest_conf = 0.0
    
    for result in results:
        boxes = result.boxes
        for box in boxes:
            conf = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            
            # Find the detection with highest confidence
            if conf > CONFIDENCE_THRESHOLD and conf > highest_conf:
                highest_conf = conf
                detected_gesture = class_name
                
            # Draw bounding box for visualization
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{class_name} {conf:.2f}", (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Note: If your YOLO model is purely an Image Classification model (predicts classes directly per frame without boxes), 
    # instead of the box iteration above, you would use:
    # probs = results[0].probs
    # if probs is not None:
    #     class_id = int(probs.top1)
    #     conf = float(probs.top1conf)
    #     class_name = model.names[class_id]
    #     if conf > CONFIDENCE_THRESHOLD:
    #         detected_gesture = class_name

    # Check and trigger the gesture action
    if detected_gesture is not None:
        execute_command(detected_gesture)
        
    # Show Cooldown Status on Screen
    time_since = time.time() - last_action_time
    if time_since < COOLDOWN_TIME:
        cv2.putText(frame, "COOLDOWN...", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        cv2.putText(frame, "READY", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
    cv2.imshow("Gesture Controlled Computer System", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
