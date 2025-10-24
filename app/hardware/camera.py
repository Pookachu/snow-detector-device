import cv2
import time

def capture_frame(save_path):
    """
    Captures a single frame from the USB camera
    Saves it to the specified 'save_path'.
    Returns true on success, False on failure.
    """
    # 0 is typically the default USB webcam

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Cannot open camera")
        return False

    # Give the camera a moment to warm up

    time.sleep(0.5)

    # Read a single frame
    ret, frame = cap.read()

    if not ret:
        print("ERROR: Can't receive frame. Exiting...")
        cap.release()
        return False

    # Save the captured frame to the file
    cv2.imwrite(save_path, frame)

    # When everything is done, release the capture
    cap.release()
    print(f"Image saved {save_path}")
    return True