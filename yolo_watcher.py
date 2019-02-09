#!/usr/bin/env python3
from pydarknet import Detector, Image
import argparse
import cv2
import os

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher:
    def __init__(self):
        self.DIRECTORY_TO_WATCH = './img'
        print('Watching \'%s\' directory for images' % self.DIRECTORY_TO_WATCH)
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif(event.event_type == 'created' and
             event.src_path.endswith(('.png', '.jpg', '.jpeg'))):
            print("Received image file %s" % event.src_path)
            process_image(event.src_path)


def process_image(image_path):
    output_dat = './dat/' + image_path.split('/')[-1] + '.dat'
    output_img = './dat/' + image_path.split('/')[-1] + '.jpg'
    img = cv2.imread(image_path)
    img2 = Image(img)
    img_width = img.shape[1]
    img_height = img.shape[0]

    results = net.detect(img2)
    output = open(output_dat, 'w')
    for cat, score, bounds in results:
        x, y, w, h = bounds
        x_scaled = float(x) / img_width
        y_scaled = float(y) / img_width
        output.write("%8s\tX:%8d\tY:%8d\n" % (str(cat), x, y))
        output.write("%8s\tX:%8d\tY:%8d\n" % ('Scaled:', x_scaled, y_scaled))
        cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0), thickness=2)
        cv2.putText(img,str(cat.decode("utf-8")),(int(x),int(y)),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0))
        cv2.imwrite(output_img, img)

    print('%d Detections logged in %s' % (len(results), output_dat))

if __name__ == "__main__":
    darknet_path = os.environ['DARKNET_HOME']
    config = os.path.join(darknet_path, 'cfg/yolov3.cfg')
    weights = os.path.join(darknet_path, 'yolov3.weights')
    coco = os.path.join(darknet_path, 'cfg/coco.data')

    net = Detector(bytes(config, encoding="utf-8"), bytes(weights, encoding="utf-8"), 0, bytes(coco, encoding="utf-8"))

    w = Watcher()
    w.run() 
