import cv2
import pyautogui
import time
from ultralytics import YOLO
import screen_brightness_control as sbc

# Configuration
MODEL_PATH = "best.pt" # Replace with your trained YOLOv8 model file
CONFIDENCE_THRESHOLD = 0.60 # Increased to 0.60 to reduce background false positives

# Specific Cooldown times per action (in seconds)
COOLDOWNS = {
    'open_palm': 2.0,     # Screenshot needs long cooldown
    'thumbs_up': 0.3,     # Volume up
    'fist': 0.1,          # Scrolling should be very fast/seamless
    'swipe_right': 0.3,   # Brightness
    'swipe_left': 0.3     # Brightness
}

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
    
    # Get the specific cooldown for this gesture (default to 1.0s just in case)
    cooldown = COOLDOWNS.get(gesture_name, 1.0)
    
    if current_time - last_action_time < cooldown:
        # Avoid spamming
        return

    print(f"Executing action for gesture: {gesture_name}")
    
    try:
        if gesture_name == 'thumbs_up':
            # Increase Volume (loop manually to ensure OS catches it)
            for _ in range(5):
                pyautogui.press('volumeup')
                time.sleep(0.01)
        
        elif gesture_name == 'open_palm':
            # Take Screenshot
            filename = f"screenshot_{int(time.time())}.png"
            pyautogui.screenshot(filename)
            print(f"Screenshot saved to {filename}")
        
        elif gesture_name == 'fist':
            # Scroll Down smoothly
            pyautogui.scroll(-200)
            
        elif gesture_name == 'swipe_right':
            # Increase Brightness
            current_brightness = sbc.get_brightness(display=0)[0]
            sbc.set_brightness(min(100, current_brightness + 10), display=0)
        
        elif gesture_name == 'swipe_left':
            # Decrease Brightness
            current_brightness = sbc.get_brightness(display=0)[0]
            sbc.set_brightness(max(0, current_brightness - 10), display=0)
    except Exception as e:
        print(f"Error executing command: {e}")
        
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
    best_box = None
    best_class_name = None
    
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
                best_box = list(map(int, box.xyxy[0]))
                best_class_name = class_name

    # Only draw bounding box for the highest confidence visualization
    if best_box is not None:
        x1, y1, x2, y2 = best_box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"{best_class_name} {highest_conf:.2f}", (x1, y1 - 10), 
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
        # Normalize the detected gesture name to match the logic (e.g. 'Thumbs Up' -> 'thumbs_up')
        normalized_gesture = detected_gesture.lower().replace(' ', '_')
        execute_command(normalized_gesture)
        
    # Show Cooldown Status on Screen
    time_since = time.time() - last_action_time
    # using a simple visual threshold of 0.5 for the visual READY indicator
    if time_since < 0.5:
        cv2.putText(frame, "ACTION ACTIVE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        cv2.putText(frame, "READY", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
    cv2.imshow("Gesture Controlled Computer System", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
