# Sweet - 2 DOF Object Tracking Pan and Tilt Mechanism

This project demonstrates a 2 Degrees of Freedom (2-DOF) pan and tilt mechanism designed to track and follow objects, such as faces, using deep learning. The system utilizes an Arduino for servo control, a main PC for object detection and localization, and a RealSense camera for capturing video streams.

View
<img width="1138" alt="Screenshot 2024-06-08 at 10 45 57 AM" src="https://github.com/abhismirai10/Sweet_a_2_dof_robotic_follower/assets/121724635/ec9d52c2-792f-4823-a581-163a11837def">

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Hardware Components](#hardware-components)
- [Software Components](#software-components)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Video Demonstration](https://youtu.be/Pwh9HPbR4ss)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction
The objective of this project is to create a pan and tilt mechanism that can follow an object, specifically a human face. This is achieved by using two servo motors to control the horizontal (pan) and vertical (tilt) movement of the camera, an Arduino for servo control, and a main PC running a deep learning algorithm to detect and localize objects in real-time.

## Features
- **Real-time Object Detection**: Utilizes OpenCV and Haar cascades for face detection.
- **2-DOF Control**: Pan and tilt mechanism controlled by two servo motors.
- **Arduino Integration**: Arduino handles servo control based on commands from the main PC.
- **3D Printed Parts**: Custom designed and 3D printed parts for mounting the camera and servos.

## Hardware Components
- 2 x Servo Motors
- 1 x Arduino (e.g., Arduino Uno)
- 1 x Intel RealSense Camera
- 3D Printed Parts for mounting and mechanism
- Connecting wires and power supply

## Software Components
- Python
- OpenCV
- pyrealsense2
- Arduino IDE

## Installation and Setup

### Hardware Setup
1. **3D Print Parts**: Print all necessary parts for the pan and tilt mechanism.
2. **Assemble Mechanism**: Attach the servo motors and RealSense camera to the 3D printed parts.
3. **Connect Servos to Arduino**:
   - Connect the yaw (pan) servo to pin 9 on the Arduino.
   - Connect the pitch (tilt) servo to pin 10 on the Arduino.
4. **Connect Arduino to PC**: Connect the Arduino to your main PC via a USB cable.

### Software Setup
1. **Clone Repository**:
   ```bash
   git clone git@github.com:abhismirai10/Sweet_a_2_dof_robotic_follower.git
   cd 2dof-object-tracking
   ```
2. **Install Dependencies**:
   ```bash
   pip install opencv-python pyrealsense2 numpy pyserial
   ```
3. **Upload Arduino Code**:
   - Open the Arduino IDE.
   - Load the `servo_control.ino` file from the `arduino` directory.
   - Select the appropriate board and port, then upload the code to the Arduino.

## Usage
1. **Run the Python Script**:
   ```bash
   python object_tracking.py
   ```
2. **Start the RealSense Camera**: Ensure the camera is properly connected and functioning.
3. **Face Detection**: The system will start detecting faces and send servo control commands to the Arduino to adjust the pan and tilt angles accordingly.
4. **Stop the Program**: Press `q` in the OpenCV window to terminate the program.

## Video Demonstration
Watch the video demonstration of the project on YouTube: [2-DOF Object Tracking Pan and Tilt Mechanism](https://youtu.be/Pwh9HPbR4ss)

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- OpenCV for the computer vision library.
- Intel for the RealSense camera.
- Arduino for the microcontroller platform.
- Special thanks to the contributors of the project.

---

Feel free to contribute to this project by opening issues or submitting pull requests. For any inquiries or feedback, please contact [abhismirai10@gmail.com].
