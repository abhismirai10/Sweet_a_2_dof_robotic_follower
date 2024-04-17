import pyrealsense2 as rs
import numpy as np
import cv2
import serial

# file for face detection 
faceCascade = cv2.CascadeClassifier('haar/haarcascade_frontalface_default.xml')

# Setup serial connection
ser = serial.Serial('/dev/ttyACM0', 9600)  # Adjust '/dev/ttyACM0' to your Arduino's port

width, height = 640, 480
fps = 30

# Configure color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, fps)

# Start streaming
pipeline.start(config)

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        
        if not color_frame:
            continue
        
        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())
        
        # Circle at the center
        cv2.circle(color_image, (int(width/2), int(height/2)), radius=3, color=(255, 0, 0), thickness=-1)
        
        # Face detection
        faces = faceCascade.detectMultiScale(color_image, 1.3, 5)
        for face in faces:
            x, y, w, h = face
            cv2.rectangle(color_image, (x, y), (x+w, y+h), (255, 0, 0), 3)
            x_center = int(x + w / 2)
            y_center = int(y + h / 2)
            cv2.circle(color_image, (x_center, y_center), radius=3, color=(0, 0, 0), thickness=-1)
            
            error_yaw = x_center - (width/2)
            error_pitch = y_center - (height/2)

            # Send center_x and center_y to Arduino
            ser.write(f"{error_yaw},{error_pitch}\n".encode())

        # Show images
        cv2.imshow('RGB Image', color_image)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop streaming
    pipeline.stop()
    cv2.destroyAllWindows()