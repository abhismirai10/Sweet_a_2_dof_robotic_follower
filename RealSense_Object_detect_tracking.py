
import pyrealsense2 as rs
import numpy as np
import cv2

#fuction to create Trackbar
class TrackbarHandler:
    def __init__(self):
        self.hue_low = 82
        self.hue_high = 125
        self.sat_low = 128
        self.sat_high = 243
        self.val_low = 154
        self.val_high = 251

    def on_hue_low(self, val):
        self.hue_low = val
        print('Hue Low', self.hue_low)

    def on_hue_high(self, val):
        self.hue_high = val
        print('Hue High', self.hue_high)

    def on_sat_low(self, val):
        self.sat_low = val
        print('Saturation Low', self.sat_low)

    def on_sat_high(self, val):
        self.sat_high = val
        print('Saturation High', self.sat_high)

    def on_val_low(self, val):
        self.val_low = val
        print('Value Low', self.val_low)

    def on_val_high(self, val):
        self.val_high = val
        print('Value High', self.val_high)

#function to initialize the trackbar
def initialize_trackbars(trackbar_handler):
    cv2.namedWindow('MyTrackbar', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('MyTrackbar', np.zeros((1, 1)))  
    cv2.moveWindow('MyTrackbar', width, 0)
    cv2.resizeWindow('MyTrackbar', width, height)

    cv2.createTrackbar('Hue Low', 'MyTrackbar', 95, 179, trackbar_handler.on_hue_low)
    cv2.createTrackbar('Hue High', 'MyTrackbar', 119, 179, trackbar_handler.on_hue_high)
    cv2.createTrackbar('Sat Low', 'MyTrackbar', 220, 255, trackbar_handler.on_sat_low)
    cv2.createTrackbar('Sat High', 'MyTrackbar', 255, 255, trackbar_handler.on_sat_high)
    cv2.createTrackbar('Val Low', 'MyTrackbar', 106, 255, trackbar_handler.on_val_low)
    cv2.createTrackbar('Val High', 'MyTrackbar', 255, 255, trackbar_handler.on_val_high)


def main():
    trackbar_handler = TrackbarHandler()

    global width, height
    width, height = 640, 480
    
    # Configure color stream
    pipeline = rs.pipeline()
    config = rs.config()

    # Get device product line for setting a supporting resolution
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()
    device_product_line = str(device.get_info(rs.camera_info.product_line))

    found_rgb = False
    for s in device.sensors:
        if s.get_info(rs.camera_info.name) == 'RGB Camera':
            found_rgb = True
            break
    if not found_rgb:
        print("The demo requires a camera with a Color sensor.")
        exit(0)

    #print(device_product_line)
    # Enable color stream
    if device_product_line == 'L500':            # # Show images
            # cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            # cv2.imshow('RealSense', color_image)
        config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
    else:
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # Start streaming
    pipeline.start(config)


    initialize_trackbars(trackbar_handler)
    
    # Main loop
    try:
        while True:
            # Wait for a coherent pair of frames: color
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue

            # Convert images to numpy arrays
            frame = np.asanyarray(color_frame.get_data())

            HSV_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # define color bounds and create mask and Countours to isolate objects of specified color
            lower_bound = np.array([trackbar_handler.hue_low, trackbar_handler.sat_low, trackbar_handler.val_low])
            upper_bound = np.array([trackbar_handler.hue_high, trackbar_handler.sat_high, trackbar_handler.val_high])
            
            mask = cv2.inRange(HSV_frame, lower_bound, upper_bound)
            contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)

            for contour in contours:
                area = cv2.contourArea(contour)
                (x,y,w,h) = cv2.boundingRect(contour)
                if area > 50:
                    cv2.rectangle(frame,(x,y), (x+w, y+h), (255,0,0), 3)
                    center_x, center_y = int(x + w/2), int(y + h/2)
                    cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)

            # apply mask to original frame to isolate object of interest
            object_of_interest = cv2.bitwise_and(frame, frame, mask=mask)

            # display the mask, object of interest, and the original frame
            cv2.imshow('frame01', frame)
            cv2.moveWindow('frame01', 0, 0)
            cv2.imshow('myMask', mask)
            cv2.moveWindow('myMask', 0, height)

            # exit program on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Stop streaming
        pipeline.stop()


if __name__ == "__main__":
    main()
