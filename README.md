# IOT Junk Sorting

## Overview
IOT Junk Sorting is an IoT-based project designed to automatically sort waste into categories such as metal and organic materials using the YOLOv3 object detection model. The project aims to educate children about waste sorting and promote environmental awareness through an intuitive, user-friendly system.

## Features
- **Automatic Waste Sorting**: Utilizes YOLOv3 and ESP32 Camera to identify and classify waste into metal and organic categories.
- **Control Interface**: Provides a Tkinter-based GUI for monitoring and managing the sorting process.
- **IoT Integration**: Connects Arduino Uno and ESP32 Camera to collect data and control hardware components like servos and a conveyor belt.

## Technologies Used
- **Hardware**:
  - Arduino Uno: Controls servos and ultrasonic sensor.
  - ESP32 Camera: Captures and processes images for waste identification.
  - Servo: Operates the sorting mechanism.
  - Ultrasonic Sensor: Detects waste on the conveyor belt.
  - Conveyor Belt: Moves waste through the sorting area.
- **Software**:
  - Python: Core logic and GUI development.
  - OpenCV with YOLOv3: Processes images and classifies waste using the YOLOv3 deep learning model.  
  - Tkinter: Graphical user interface for monitoring.
  - ESP32 WiFiCam Server Library: Handles ESP32 Camera communication.
  - PySerial: Facilitates communication between Python and Arduino.
- **IoT Communication**:
  - HTTP (RESTful API): Transfers data between ESP32 Camera and the control system.

## Installation
### Requirements
- Arduino IDE for programming Arduino Uno.
- Python 3.x with libraries: `opencv-python`, `pyserial`, `tkinter`.
- Hardware: Arduino Uno, ESP32 Camera, servo, ultrasonic sensor, conveyor belt.
- Pre-trained YOLOv3 model weights and configuration files (module/coco.name, yolov3.weights, yolov3.cfg).

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/vao211/IOT_junk_sorting
   cd IOT_junk_sorting
   ```
2. **Install Python Libraries**:
   ```bash
   pip install opencv-python pyserial tk
   ```
3. **Hardware Setup**:
   - Connect Arduino Uno to servo and ultrasonic sensor as per the schematic.
   - Configure ESP32 Camera with the appropriate firmware from ESP32 WiFiCam Server Library.
   - Set up the conveyor belt with Arduino Uno for movement control.
4. **Upload Arduino Code**:
   - Open `Arduino/Uno/uno/uno.ino` file in Arduino IDE.
   - Upload the code to Arduino Uno.
5. **Run the Python Application**:
   - Update the ESP32 Camera IP address, COM, in the app.py.
   - Run the main script:
     ```bash
     python app.py
     ```

## Usage
1. **Start the System**:
   - Connect the hardware and run `app.py` to launch the application.
   - The Tkinter GUI will display the sorting status and control options.
2. **Sort Waste**:
   - Place waste on the conveyor belt; the ultrasonic sensor detects it and triggers the ESP32 Camera.
   - The camera captures images, and OpenCV classifies the waste as metal or organic.
   - The servo moves the waste to the appropriate bin.
3. **Monitor**:
   - Use the Tkinter GUI to view sorting status and statistics.
