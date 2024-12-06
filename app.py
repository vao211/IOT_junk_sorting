import cv2
import numpy as np
import logging
import json
import urllib.request
import serial
import time
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd

url = 'http://192.168.1.4/480x320.jpg'

unsed = ['tvmonitor','toothbrush','diningtable','bed', 'pottedplant',
         'orange','traffic light', 'train','sports ball','truck',
         'refrigerator',]
Inorganic = [
    'bicycle', 'car', 'motorbike', 'aeroplane', 'bus',
    'boat', 'fire hydrant',
    'stop sign', 'parking meter', 'bench', 'backpack', 'umbrella',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard',
    'kite', 'baseball bat', 'baseball glove',
    'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass',
    'cup', 'fork', 'knife', 'spoon', 'bowl', 'chair', 'sofa',
    'toilet',
    'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'book',
    'clock', 'vase', 'scissors', 'teddy bear',
]
Organic = [
    'banana', 'apple', 'sandwich',  'broccoli',
    'carrot', 'hot dog', 'pizza', 'donut', 'cake', 
    'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 
    'bear', 'zebra', 'giraffe',
]

arduino_port = 'COM15' 
baud_rate = 9600
arduino = serial.Serial(arduino_port, baud_rate)

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

whT = 224
confident = 0.5
nonMaxSupr = 0.3
classesfile = 'module/coco.names'
modelConfig = 'module/yolov3.cfg'
modelWeights = 'module/yolov3.weights'

with open(classesfile, 'rt', encoding='utf-8') as f:
    classNames = f.read().rstrip('\n').split('\n')

net = cv2.dnn.readNetFromDarknet(modelConfig, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

json_file_path = 'Export/detected_objects.json'

def write_to_json(data):
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

        
excel_file_path = 'Export/dectected_objects.xlsx'
def export_to_excel():
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        df = pd.DataFrame.from_dict(data, orient='index')

        df.to_excel(excel_file_path, index=True, sheet_name='Detected Objects')
        messagebox.showinfo("Export Successful", f"Data exported to {excel_file_path} successfully.")
    except Exception as e:
        logging.error(f"Error exporting to Excel: {e}")
        
        
def findObjects(outputs, img):
    global detected_objects
    hT, wT, _ = img.shape
    bbox, classIds, confs = [], [], []

    for output in outputs:
        for det in output:     #list obj
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confident:
                w, h = int(det[2] * wT), int(det[3] * hT)
                x, y = int((det[0] * wT) - w / 2), int((det[1] * hT) - h / 2)
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))

    indices = cv2.dnn.NMSBoxes(bbox, confs, confident, nonMaxSupr)

    if indices is not None and len(indices) > 0:
        for i in indices.flatten():
            box = bbox[i]
            x, y, w, h = box
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
            label = f'{classNames[classIds[i]].upper()} {int(confs[i] * 100)}%'
            cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

            object_name = classNames[classIds[i]]
            object_type = 'Organic' if object_name in Organic else 'Inorganic'
            if object_name in Organic:
                object_type = 'Organic'
            elif object_name in Inorganic:
                object_type = 'Inorganic'
            
            if object_name in Organic or object_name in Inorganic:
                if object_name in Organic:
                    arduino.write('1'.encode())
                    print(object_name)
                    print("send 1")
                    time.sleep(2)
                elif object_name in Inorganic:
                    arduino.write('2'.encode())
                    print(object_name)
                    print("send 2")
                    time.sleep(2)

                detected_objects[object_name] = {
                    'count': detected_objects.get(object_name, {'count': 0})['count'] + 1,
                    'type': object_type
                }
    write_to_json(detected_objects)

def get_frame_url(url):
    try:
        img_resp = urllib.request.urlopen(url)
        img_np = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        logging.error(f"Error fetching image: {e}")
        return None

def detection_thread():
    global detected_objects
    detected_objects = {}


    while True:
        img = get_frame_url(url)
        if img is None:
            continue
        
        #OpenCV procesing image
        blob = cv2.dnn.blobFromImage(img, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)  #2chuẩn hóa về 0-1
        net.setInput(blob)
        layernames = net.getLayerNames()
        outputNames = [layernames[i - 1] for i in net.getUnconnectedOutLayers().flatten()]
        outputs = net.forward(outputNames)

        findObjects(outputs, img)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(image=img)

        video_label.imgtk = img_tk
        video_label.configure(image=img_tk)

        window.update()

def start():
    detection = threading.Thread(target=detection_thread)
    detection.daemon = True
    time.sleep(1)
    detection.start()

def close():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        arduino.close()
        window.destroy()

window = tk.Tk()
window.title("Object sorting App")

window_width = 720
window_height = 550

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

video_label = tk.Label(window)
video_label.pack()

start_button = tk.Button(window, text="Start", command=start)
start_button.pack(pady=20)

quit_button = tk.Button(window, text="Quit", command=close)
quit_button.pack(pady=20)

#Export button
export_button = tk.Button(window, text="Export to Excel", command=export_to_excel)
export_button.pack(pady=20)

window.protocol("WM_DELETE_WINDOW", close)

window.mainloop()