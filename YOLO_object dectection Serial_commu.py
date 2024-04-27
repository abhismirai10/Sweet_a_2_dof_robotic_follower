#here communication is 120,90 just that yaw,pitch 
from ultralytics import YOLO
import pyrealsense2 as rs
import numpy as np
import cv2
import serial

#load the model
model = YOLO('yolov8n.pt')

# Setup serial connection
ser = serial.Serial('/dev/ttyACM0', 9600)  # Adjust '/dev/ttyACM0' to your Arduino's port

width, height = 640, 480
fps =30

#for camera feed
# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
#config.enable_stream(rs.stream.depth, width, height, rs.format.z16, fps)
config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, fps)

# Start streaming
pipeline.start(config)

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        #depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        
        #not depth_frame or 
        if not color_frame:
            continue
        
        # Convert images to numpy arrays
        #depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        
        # Apply colormap on depth image (optional)
        #depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        #circle at the center
        cv2.circle(color_image, (int(width/2), int(height/2)), radius=3, color=(255, 0, 0), thickness=-1)
        
        #for tracking the object from the frame
        results = model.track(color_image, persist=True)

        #to find coordinate of center of detected object
        for result in results:
            boxes = result.boxes.cpu().numpy()
            xyxys = boxes.xyxy
            class_ids = boxes.cls

            #now lets seperate all the bounding box in one frame
            for class_id, xyxy in zip(class_ids, xyxys):
                if class_id == 67:
                    x1, y1, x2, y2 = xyxy
                    x_center = int(x1 + (abs(x1-x2)) / 2)
                    y_center = int(y1 + (abs(y1-y2)) / 2)
                    print(x_center, y_center, class_id)
                    cv2.circle(color_image, (x_center, y_center), radius=3, color=(0, 0, 0), thickness=-1)
                    
                    error_yaw = x_center - (width/2)
                    error_pitch = y_center - (height/2)

                    # Send center_x and center_y to Arduino
                    ser.write(f"{error_yaw},{error_pitch}\n".encode())

        object_detection_frame = results[0].plot()

        # Show images
        cv2.imshow('RGB Image', color_image)
        #cv2.imshow('object detection', object_detection_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop streaming
    pipeline.stop()
    cv2.destroyAllWindows()
