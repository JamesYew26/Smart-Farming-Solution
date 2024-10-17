import cv2

# Open the default camera (0). Change the index if multiple cameras are available.
cam = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cam.isOpened():
    print("Error: Could not open camera.")
    exit()

# Capture a single frame
ret, image = cam.read()

# Check if the frame was successfully captured
if not ret:
    print("Error: Failed to capture image.")
else:
    # Display the captured image in a window
    cv2.imshow('Captured Image', image)
    
    # Wait for a key press to close the display window
    cv2.waitKey(0)

    # Define the path to save the image on the Desktop
    save_path = '/home/pi/Desktop/FYP/testimage.jpg'
    
    # Save the captured image to the specified path
    cv2.imwrite(save_path, image)
    print(f"Image saved to {save_path}")

# Release the camera and close all OpenCV windows
cam.release() 
cv2.destroyAllWindows()
