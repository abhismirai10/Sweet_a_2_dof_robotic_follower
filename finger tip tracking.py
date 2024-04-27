import pyrealsense2 as rs
import numpy as np
import cv2
import serial
import mediapipe as mp

# File for face detection
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

# Class for handling hand detection and landmark detection
class HandDetector:
    def __init__(self, static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp = mp.solutions
        self.hand_detector = self.mp.hands.Hands(static_image_mode=static_image_mode,
                                                max_num_hands=max_num_hands,
                                                min_detection_confidence=min_detection_confidence,
                                                min_tracking_confidence=min_tracking_confidence)
        self.landmark_drawer = self.mp.drawing_utils

    # Method to process a frame, detect hands and draw landmarks
    def detect_and_draw_landmarks(self, frame):
        hand_positions = []

        # Process the frame to find hand landmarks
        hand_landmarks_result = self.hand_detector.process(frame)

        # If hand landmarks are detected, draw them on the frame
        if hand_landmarks_result.multi_hand_landmarks:
            for hand_landmark in hand_landmarks_result.multi_hand_landmarks:
                self.landmark_drawer.draw_landmarks(frame, hand_landmark, self.mp.hands.HAND_CONNECTIONS)
                landmarks_coordinates = [(int(landmark.x * width), int(landmark.y * height)) for landmark in hand_landmark.landmark]
                hand_positions.append(landmarks_coordinates)
        return hand_positions

# Create a HandDetector object
hand_detector = HandDetector()

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            continue

        # Convert color frame to numpy array
        color_image = np.asanyarray(color_frame.get_data())

        # Circle at the center
        cv2.circle(color_image, (int(width/2), int(height/2)), radius=3, color=(255, 0, 0), thickness=-1)

        # Get hand landmarks from the frame
        hand_landmarks = hand_detector.detect_and_draw_landmarks(color_image)

        # Use landmark positions
        for hand_landmark in hand_landmarks:
            point = 4
            x_center, y_center = hand_landmark[point]
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
