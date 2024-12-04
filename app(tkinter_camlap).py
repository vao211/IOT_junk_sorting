import cv2
import numpy as np
import logging
import serial
import json
import tkinter as tk
from tkinter import Label, messagebox
from threading import Thread
from PIL import Image, ImageTk
import time
import pandas as pd

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

Inorganic = [
    'bicycle', 'car', 'motorbike', 'aeroplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant',
    'stop sign', 'parking meter', 'bench', 'backpack', 'umbrella',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard',
    'sports ball', 'kite', 'baseball bat', 'baseball glove',
    'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass',
    'cup', 'fork', 'knife', 'spoon', 'bowl', 'chair', 'sofa',
    'pottedplant', 'bed', 'diningtable', 'toilet', 'tvmonitor',
    'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book',
    'clock', 'vase', 'scissors', 'teddy bear'
]
Organic = [
    'banana', 'apple', 'sandwich', 'orange', 'broccoli',
    'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'person', 
    'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 
    'bear', 'zebra', 'giraffe'
]

whT = 224
confThreshold = 0.7
nmsThreshold = 0.4
classesfile = 'coco.names'
modelConfig = 'yolov3.cfg'
modelWeights = 'yolov3.weights'

with open(classesfile, 'rt', encoding='utf-8') as f:
    classNames = f.read().rstrip('\n').split('\n')

net = cv2.dnn.readNetFromDarknet(modelConfig, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

arduino_port = 'COM15'
baud_rate = 9600
arduino = serial.Serial(arduino_port, baud_rate)

json_file_path = 'detected_objects.json'

def write_to_json(data):
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

excel_file_path = 'dectected_objects.xlsx'
def write_to_json(data):
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        
def export_to_excel():
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        df = pd.DataFrame.from_dict(data, orient='index')

        df.to_excel(excel_file_path, index=True, sheet_name='Detected Objects')
        messagebox.showinfo("Export Successful", f"Data exported to {excel_file_path} successfully.")
    except Exception as e:
        logging.error(f"Error exporting to Excel: {e}")

class ObjectDetectionApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Object Detection")
        
        self.label = Label(window)
        self.label.pack()
        
        self.cap = cv2.VideoCapture(0)
        self.running = True
        self.detected_objects = {}
        
        self.window.bind('<q>', self.quit)

        self.thread = Thread(target=self.video_stream)
        self.thread.start()

    def find_objects(self, outputs, img):
        hT, wT, _ = img.shape
        bbox, classIds, confs = [], [], []

        for output in outputs:
            for det in output:
                scores = det[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > confThreshold:
                    w, h = int(det[2] * wT), int(det[3] * hT)
                    x, y = int((det[0] * wT) - w / 2), int((det[1] * hT) - h / 2)
                    bbox.append([x, y, w, h])
                    classIds.append(classId)
                    confs.append(float(confidence))

        indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)

        if indices is not None and len(indices) > 0:
            for i in indices.flatten():
                box = bbox[i]
                x, y, w, h = box
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
                label = f'{classNames[classIds[i]].upper()} {int(confs[i] * 100)}%'
                cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

                object_name = classNames[classIds[i]]
                object_type = 'Organic' if object_name in Organic else 'Inorganic'
                
                self.detected_objects[object_name] = {
                    'count': self.detected_objects.get(object_name, {'count': 0})['count'] + 1,
                    'type': object_type
                }

                if object_name in Organic:
                    time.sleep(0.2)
                    arduino.write('1'.encode())
                    time.sleep(0.6)
                    
                elif object_name in Inorganic:
                    time.sleep(0.3)
                    arduino.write('2'.encode())
                    time.sleep(0.6)
        write_to_json(self.detected_objects)

    def video_stream(self):
        while self.running:
            ret, img = self.cap.read()
            if not ret:
                logging.error("Failed to grab frame.")
                break
            
            blob = cv2.dnn.blobFromImage(img, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)
            net.setInput(blob)
            layernames = net.getLayerNames()
            outputNames = [layernames[i - 1] for i in net.getUnconnectedOutLayers().flatten()]
            outputs = net.forward(outputNames)

            self.find_objects(outputs, img)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)
            self.label.update()

        self.cap.release()

    def quit(self, event=None):
        self.running = False
        self.window.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = ObjectDetectionApp(root)
    #Add an Export button
    export_button = tk.Button(root, text="Export to Excel", command=export_to_excel)
    export_button.pack(pady=20)
    root.protocol("WM_DELETE_WINDOW", app.quit)
    root.mainloop()