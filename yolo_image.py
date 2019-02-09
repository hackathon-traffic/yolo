#!/usr/bin/env python3
from pydarknet import Detector, Image
import argparse
import cv2
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process an image.')
    parser.add_argument('path', metavar='image_path', type=str, help='Path to source image')
    parser.add_argument('output', metavar='output_path', type=str, help='Data file for output')
    args = parser.parse_args()

    darknet_path = os.environ['DARKNET_HOME']
    config = os.path.join(darknet_path, 'cfg/yolov3.cfg')
    weights = os.path.join(darknet_path, 'yolov3.weights')
    coco = os.path.join(darknet_path, 'cfg/coco.data')

    net = Detector(bytes(config, encoding="utf-8"), bytes(weights, encoding="utf-8"), 0, bytes(coco, encoding="utf-8"))

    img = cv2.imread(args.path)

    img2 = Image(img)

    # r = net.classify(img2)
    results = net.detect(img2)

    output = open(args.output, 'w')

    for cat, score, bounds in results:
        x, y, w, h = bounds
        output.write("%s at X: %d\tY: %d\n" % (str(cat), x, y))
        cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0), thickness=2)
        cv2.putText(img,str(cat.decode("utf-8")),(int(x),int(y)),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0))

    print('%d Detections logged in %s' % (len(results), args.output))
    cv2.imshow("output", img)
    cv2.imwrite("output.jpg", img)
    cv2.waitKey(0)
