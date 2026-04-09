import cv2
import os

# Define the gestures we want to collect data for
GESTURES = ['thumbs_up', 'open_palm', 'fist', 'swipe_right', 'swipe_left']
DATA_DIR = 'dataset/images'

# Create directories for saving images
for gesture in GESTURES:
    os.makedirs(os.path.join(DATA_DIR, gesture), exist_ok=True)

cap = cv2.VideoCapture(0)

# Settings
current_gesture_index = 0
img_count = 0

print("=== Gesture Data Collection ===")
print("Instructions:")
print("- Press 'n' to switch to the NEXT gesture.")
print("- Press 's' to SAVE an image for the current gesture.")
print("- Press 'q' to QUIT the program.")
print("===============================\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1) # Mirror the frame
    
    current_gesture = GESTURES[current_gesture_index]

    # Display UI
    cv2.putText(frame, f"Gesture: {current_gesture}", (20, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Count: {img_count}", (20, 80), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the frame
    cv2.imshow("Data Collection", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        # Quit
        break
    elif key == ord('n'):
        # Next Gesture class
        current_gesture_index = (current_gesture_index + 1) % len(GESTURES)
        # Recalculate img_count for new gesture
        current_gesture = GESTURES[current_gesture_index]
        existing_files = os.listdir(os.path.join(DATA_DIR, current_gesture))
        img_count = len(existing_files)
        print(f"Switched to: {current_gesture}")
    elif key == ord('s'):
        # Save frame
        img_path = os.path.join(DATA_DIR, current_gesture, f"{current_gesture}_{img_count}.jpg")
        cv2.imwrite(img_path, frame)
        print(f"Saved: {img_path}")
        img_count += 1

cap.release()
cv2.destroyAllWindows()
